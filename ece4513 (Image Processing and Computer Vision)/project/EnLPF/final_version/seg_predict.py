import os
import time
import csv
import logging
from PIL import Image
import numpy as np
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms

from seg.defaults import _C as cfg
from seg.defaults import SEG_MODEL_ENCODER_PATH, SEG_MODEL_DECODER_PATH
from seg.models import ModelBuilder, SegmentationModule
from seg.lib.nn import async_copy_to

__all__ = ["seg_predict"]

logging.basicConfig(level=logging.DEBUG)

class seg_predict(object):
    def __init__(self, root=os.path.join(os.getcwd(),"seg")):
        torch.cuda.set_device(0)
        # self.colors = loadmat(os.path.join(root,'data/color150.mat'))['colors']
        self.names = {}
        with open(os.path.join(root, 'data/object150_info.csv')) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.names[int(row[0])] = row[5].split(";")[0]
        cfg.merge_from_file(os.path.join(root, "config/ade20k-resnet50dilated-ppm_deepsup.yaml"))
        cfg.MODEL.arch_encoder = cfg.MODEL.arch_encoder.lower()
        cfg.MODEL.arch_decoder = cfg.MODEL.arch_decoder.lower()
        # absolute paths of model weights
        cfg.MODEL.weights_encoder = SEG_MODEL_ENCODER_PATH
        cfg.MODEL.weights_decoder = SEG_MODEL_DECODER_PATH

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
        self.segmentation_module = SegmentationModule(net_encoder, net_decoder, crit).cuda().eval()
        self.cfg = cfg
        # self.imgSizes = (300, 375, 450, 525, 600)
        self.imgSizes = (256,)
        self.imgMaxSize = 1000
        self.matrix_channel = 1024
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    def round2nearest_multiple(self, x, p):
        return ((x - 1) // p + 1) * p

    def imresize(self, im, size, interp='bilinear'):
        if interp == 'nearest':
            resample = Image.NEAREST
        elif interp == 'bilinear':
            resample = Image.BILINEAR
        elif interp == 'bicubic':
            resample = Image.BICUBIC
        else:
            raise Exception('resample method undefined!')
        return im.resize(size, resample)

    def img_transform(self, img):
        # 0-255 to 0-1
        img = np.float32(np.array(img)) / 255.
        img = img.transpose((2, 0, 1))
        img = self.normalize(torch.from_numpy(img.copy()))
        return img

    def predict(self, img_batch: torch.Tensor):
        return self.segmentation_module(img_batch, channel_num = self.matrix_channel, segSize = (32,32))
        