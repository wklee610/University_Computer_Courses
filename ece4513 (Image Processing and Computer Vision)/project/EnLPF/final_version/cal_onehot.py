# System libs
import os
import time
import torch
import logging
import argparse
from tqdm import tqdm
from scipy.stats import entropy

# Numerical libs
import numpy as np
from PIL import Image
from seg_predict import seg_predict
from seg.lib.utils import as_numpy

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
logging.basicConfig(level=logging.DEBUG)
logging.info('current time is {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def get_img_list(path):
    path = path
    is_image_file = lambda x : any(x.endswith(extension)
                                   for extension in ['jpg', 'png', 'gif', 'bmp', 'tif'])
    return [os.path.join(r, i) for r, _, f in os.walk(path) for i in f if is_image_file(i)]



def main(imgs:list, root:str, img_path:str):
    model = seg_predict(root=os.path.join(os.getcwd(), "seg"))
    dataset_name = img_path.split('/')[-1]
    dataset_storepath = os.path.join(root,dataset_name)
    if not os.path.exists(dataset_storepath):
        '''
            create folder path for each classes
        '''
        for name in os.listdir(img_path+'/train'):
            os.makedirs(os.path.join(dataset_storepath+'/res'+'/train'+'/'+name)) 
            os.makedirs(os.path.join(dataset_storepath+'/res'+'/val'+'/'+name)) #since we do not do the training for seg
            os.makedirs(os.path.join(dataset_storepath+'/etr'+'/train'+'/'+name)) #since we do not do the training for seg
            os.makedirs(os.path.join(dataset_storepath+'/etr'+'/val'+'/'+name)) #since we do not do the training for seg
            
    for _, img_path in enumerate(tqdm(imgs)): # img_path = '/data/dataset/Places365-14/train/kitchen/00000075.jpg'
        try:
            res, temp = model.predict(img_path)
            res = as_numpy(res)
            temp = as_numpy(temp)
            res = np.squeeze(res)
            temp = np.squeeze(temp)
            I = entropy(temp,axis=0)
            res_entropy = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
            tail = img_path.split('/')[-4:]  # tail = ['Places365-14', 'train', 'kitchen', '00000075.jpg']
            im1 = Image.fromarray(res_entropy)
            im1.save(os.path.join(dataset_storepath,'etr',tail[-3],tail[-2], tail[-1].split('.')[0]+'.png'))
            im2 = Image.fromarray(res.astype(np.uint8))
            im2.save(os.path.join(dataset_storepath,'res',tail[-3],tail[-2], tail[-1].split('.')[0]+'.png'))
            
            
        except RuntimeError as exception:
            if "out of memory" in str(exception):
                print("WARNING: out of memory")
                print("The image %s is skipped since memory run out"%img_path)
                if hasattr(torch.cuda, 'empty_cache'):
                    torch.cuda.empty_cache()
            else:
                raise exception
            continue



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PyTorch Semantic Segmentation Testing"
    )
    parser.add_argument(
        "--imgs",
        default='',
        required=True,
        type=str,
        help="directory of dataset"
    )
    parser.add_argument(
        "--root",
        default='',
        required=True,
        type=str,
        help="directory of folder to store json files"
    )
    args = parser.parse_args()


    # generate testing image list
    if os.path.isdir(args.imgs):  # folder
        imgs = get_img_list(args.imgs)
    else:  # single image file
        imgs = [args.imgs]

    root = args.root  # 'seg_result/'

    main(imgs, root, args.imgs)


