# System libs
import os
import argparse
import time
from distutils.version import LooseVersion
# Numerical libs
import numpy as np
import torch
import torch.nn as nn
from scipy.io import loadmat
import csv
# Our libs
from dataset import TestDataset
from models import ModelBuilder, SegmentationModule
from utils import colorEncode, find_recursive, setup_logger
from lib.nn import user_scattered_collate, async_copy_to
from lib.utils import as_numpy
from PIL import Image
from tqdm import tqdm
from config import cfg
import json
import datetime

colors = loadmat('data/color150.mat')['colors']
names = {}
with open('data/object150_info.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        names[int(row[0])] = row[5].split(";")[0]


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.__str__()
        else:
            return super(MyEncoder, self).default(obj)

def save_dict(filename, dic):
    '''save dict into json file'''
    if not os.path.exists(filename):
        with open(filename,'w') as json_file:
            json.dump(dic, json_file, ensure_ascii=False, cls=JsonEncoder)
        
def load_dict(filename):
    '''load dict from json file'''
    with open(filename,"r") as json_file:
        dic = json.load(json_file)
    return dic

def get_img_list(path):
    is_image_file = lambda x : any(x.endswith(extension)
                                   for extension in ['jpg', 'png', 'gif', 'bmp'])
    return [os.path.join(r, i) for r, _, f in os.walk(path) for i in f if is_image_file(i)]

def visualize_result(pred, cfg, index):
#    (img, info) = data

    # print predictions in descending order
    pred = np.int32(pred)
    pixs = pred.size

    uniques, counts = np.unique(pred, return_counts=True)
    things=[0]*150
    nm = []
    for idx in np.argsort(counts)[::-1]:
        name = names[uniques[idx] + 1]
        ratio = counts[idx] / pixs * 100
        if ratio > 0.1:
            things[uniques[idx]]=1
            nm.append(name)
#            print("  {}: {:.2f}%".format(name, ratio)
        else:
            break
    #print(nm)
    p = index.split('/')[-1]
    #print(p)
    proba[p]=things


def predict(img):
    torch.cuda.set_device(gpu)

    # Network Builders
    net_encoder = ModelBuilder.build_encoder(
        arch=cfg.MODEL.arch_encoder,
        fc_dim=cfg.MODEL.fc_dim,
        weights=cfg.MODEL.weights_encoder)
    net_decoder = ModelBuilder.build_decoder(
        arch=cfg.MODEL.arch_decoder,
        fc_dim=cfg.MODEL.fc_dim,
        num_class=cfg.DATASET.num_class,
        weights=cfg.MODEL.weights_decoder,
        use_softmax=True)

    crit = nn.NLLLoss(ignore_index=-1)

    segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)
    print(cfg.DATASET)
    # Dataset and Loader
    dataset_test = TestDataset(
        cfg.list_test,
        cfg.DATASET)
    loader_test = torch.utils.data.DataLoader(
        dataset_test,
        batch_size=cfg.TEST.batch_size,
        shuffle=False,
        collate_fn=user_scattered_collate,
        num_workers=2,
        drop_last=True)
    segmentation_module.cuda()


    

def test(segmentation_module, loader, gpu):
    segmentation_module.eval()

    pbar = tqdm(total=len(loader))
    for batch_data in loader:
        # process data
        batch_data = batch_data[0]
        segSize = (batch_data['img_ori'].shape[0],
                   batch_data['img_ori'].shape[1])
        img_resized_list = batch_data['img_data']

        with torch.no_grad():
            scores = torch.zeros(1, cfg.DATASET.num_class, segSize[0], segSize[1])
            feature = torch.zeros(1, 512, segSize[0], segSize[1])
            # mark
            channels = feature.shape[1]
            scores = async_copy_to(scores, gpu)
            feature = async_copy_to(feature, gpu)
            # (304, 304), (376, 376), (456, 456), (528, 528), (600, 600)
            # (300, 375, 450, 525, 600)

            for img in img_resized_list:
                feed_dict = batch_data.copy()
                feed_dict['img_data'] = img
                del feed_dict['img_ori']
                del feed_dict['info']
                feed_dict = async_copy_to(feed_dict, gpu)
                # forward pass torch.Size([1, 150, 256, 256]) N*C*H*W
                pred_tmp, pred_tmp_feature_map = segmentation_module(feed_dict, segSize=segSize)
                if args.onehot_matrix != '':
                    feature = feature + pred_tmp_feature_map / len(cfg.DATASET.imgSizes)
                scores = scores + pred_tmp / len(cfg.DATASET.imgSizes)

            s, pred = torch.max(scores, dim=1)
            if args.onehot_matrix != '':
                obj_matrix_map = torch.zeros(cfg.DATASET.num_class, channels)
                obj_matrix_map = async_copy_to(obj_matrix_map, gpu)
                pred_vec = pred.view(1, -1)
                pred_mat = pred_vec.repeat(channels, 1)
                s = s.view(1, -1)
                feature = feature.view(channels, -1)
                for i in range(150):
                    m_vec = torch.eq(pred_vec, i)
                    m_mat = torch.eq(pred_mat, i)
                    score = s[m_vec].view(-1, 1)
                    if score.sum() <= 0:
                        continue
                    chosen = feature[m_mat].view(channels, -1)
                    vec =  torch.mm(chosen, score) / score.sum()
                    obj_matrix_map[i] = vec.view(1, -1)
                obj_map1 = torch.zeros(cfg.DATASET.num_class, channels)
                obj_map1 = async_copy_to(obj_map1, gpu)
                obj_matrix_map = as_numpy(obj_matrix_map)
            pred = as_numpy(pred.squeeze(0))

        pred = np.int32(pred)
        pixs = pred.size

        uniques, counts = np.unique(pred, return_counts=True)
        things = [0] * 150
        pred_labels = []
        for idx in np.argsort(counts)[::-1]:
            name = names[uniques[idx] + 1]
            ratio = counts[idx] / pixs * 100
            if ratio > 0.1:
                things[uniques[idx]] = 1
                pred_labels.append(name)
            else:
                break
       
        img_name = batch_data['info']
        
        pbar.update(1)
        

def main(cfg, gpu):
    torch.cuda.set_device(gpu)

    # Network Builders
    net_encoder = ModelBuilder.build_encoder(
        arch=cfg.MODEL.arch_encoder,
        fc_dim=cfg.MODEL.fc_dim,
        weights=cfg.MODEL.weights_encoder)
    net_decoder = ModelBuilder.build_decoder(
        arch=cfg.MODEL.arch_decoder,
        fc_dim=cfg.MODEL.fc_dim,
        num_class=cfg.DATASET.num_class,
        weights=cfg.MODEL.weights_decoder,
        use_softmax=True)

    crit = nn.NLLLoss(ignore_index=-1)

    segmentation_module = SegmentationModule(net_encoder, net_decoder, crit)
    print(cfg.DATASET)
    # Dataset and Loader
    dataset_test = TestDataset(
        cfg.list_test,
        cfg.DATASET)
    loader_test = torch.utils.data.DataLoader(
        dataset_test,
        batch_size=cfg.TEST.batch_size,
        shuffle=False,
        collate_fn=user_scattered_collate,
        num_workers=12,
        drop_last=True)
    segmentation_module.cuda()

    # Main loop
    test(segmentation_module, loader_test, gpu)

    print('Inference done!')
#    print(now)

if __name__ == '__main__':
    assert LooseVersion(torch.__version__) >= LooseVersion('0.4.0'), \
        'PyTorch>=0.4.0 is required'

    parser = argparse.ArgumentParser(
        description="PyTorch Semantic Segmentation Testing"
    )
    parser.add_argument(
        "--imgs",
        default='',
        required=True,
        type=str,
        help="dataset"
    )
    parser.add_argument(
        "--onehot",
        default="",
        help="ont hot cls"
    )
    parser.add_argument(
        "--cfg",
        default="config/ade20k-resnet50dilated-ppm_deepsup.yaml",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    parser.add_argument(
        "--gpu",
        default=0,
        type=int,
        help="gpu id for evaluation"
    )
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()

    cfg.merge_from_file(args.cfg)
    cfg.merge_from_list(args.opts)
    # cfg.freeze()

    logger = setup_logger(distributed_rank=0)   # TODO
    logger.info("Loaded configuration file {}".format(args.cfg))
    logger.info("Running with config:\n{}".format(cfg))

    cfg.MODEL.arch_encoder = cfg.MODEL.arch_encoder.lower()
    cfg.MODEL.arch_decoder = cfg.MODEL.arch_decoder.lower()

    # absolute paths of model weights
    cfg.MODEL.weights_encoder = os.path.join(
        cfg.DIR, 'encoder_' + cfg.TEST.checkpoint)
    cfg.MODEL.weights_decoder = os.path.join(
        cfg.DIR, 'decoder_' + cfg.TEST.checkpoint)

    assert os.path.exists(cfg.MODEL.weights_encoder) and \
        os.path.exists(cfg.MODEL.weights_decoder), "checkpoint does not exitst!"


    # generate testing image list
    if os.path.isdir(args.imgs):
        imgs = get_img_list(args.imgs)
    else:
        imgs = [args.imgs]
    # imgs=imgs[:10]
    assert len(imgs), "imgs should be a path to image (.jpg) or directory."
    cfg.list_test = [{'fpath_img': x} for x in imgs]

    if not os.path.isdir(cfg.TEST.result):
        os.makedirs(cfg.TEST.result)
    proba={}
    proba_vec={}
    proba_vec_exp1={}
    main(cfg, args.gpu)
