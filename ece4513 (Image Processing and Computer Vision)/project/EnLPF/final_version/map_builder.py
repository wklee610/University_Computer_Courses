# System libs
import os
import torch
import torchvision.transforms as transforms

from tqdm import tqdm
from scipy.stats import entropy


# Numerical libs
import numpy as np
from PIL import Image
from seg_predict import seg_predict
from seg.lib.utils import as_numpy
from utils import ImageFolderWithPaths


os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def get_img_list(path):
    path = path
    is_image_file = lambda x : any(x.endswith(extension)
                                   for extension in ['jpg', 'png', 'gif', 'bmp', 'tif'])
    return [os.path.join(r, i) for r, _, f in os.walk(path) for i in f if is_image_file(i)]


def load_sun_rgbd(store_path:str, batchsize=32, worker_number = 4):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    train_dataset = ImageFolderWithPaths(store_path+'/train', transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        normalize,
    ]))
    val_dataset = ImageFolderWithPaths(store_path+'/val', transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        normalize,
    ]))
    
    train_loader = torch.utils.data.DataLoader(train_dataset,
        batch_size = batchsize, shuffle=False,
        num_workers = worker_number, pin_memory=True)
    val_loader = torch.utils.data.DataLoader(val_dataset,
        batch_size = batchsize, shuffle=False,
        num_workers = worker_number, pin_memory=True)
    
    return train_loader, val_loader
    

def map_builder(store_root:str = 'seg_result/', img_path:str = '/data/dataset/SUN_RGBD'):
    model = seg_predict()
    dataset_name = img_path.split('/')[-1]
    dataset_storepath = os.path.join(store_root,dataset_name)
    if not os.path.exists(dataset_storepath):
        '''
            create folder path for each classes
        '''
        for name in os.listdir(img_path+'/train'):
            os.makedirs(os.path.join(dataset_storepath+'/res'+'/train'+'/'+name)) 
            os.makedirs(os.path.join(dataset_storepath+'/res'+'/val'+'/'+name)) #since we do not do the training for seg
            os.makedirs(os.path.join(dataset_storepath+'/etr'+'/train'+'/'+name)) #since we do not do the training for seg
            os.makedirs(os.path.join(dataset_storepath+'/etr'+'/val'+'/'+name)) #since we do not do the training for seg
    train_data, test_data = load_sun_rgbd('/data/dataset/SUN_RGBD')
    
    for _, (batch_img, _, file_path) in enumerate(tqdm(train_data)): # img_path = '/data/dataset/Places365-14/train/kitchen/00000075.jpg'
        batch_img = batch_img.cuda()
        res, _ = model.predict(batch_img)
        temp = as_numpy(res)
        res = as_numpy(torch.argmax(res, axis=1))
        I = entropy(temp,axis=1)
        res_entropy = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
        for _, (res_img, etr_img, path) in enumerate(zip(res, res_entropy, file_path)):
            tail = path.split('/')[-3:]  # tail = ['train', 'kitchen', '00000075.jpg']
            im1 = Image.fromarray(etr_img)
            im1.save(os.path.join(dataset_storepath,'etr',tail[0],tail[1], tail[2]))
            im2 = Image.fromarray(res_img.astype(np.uint8))
            im2.save(os.path.join(dataset_storepath,'res',tail[0],tail[1], tail[2]))
    
    for _, (batch_img, _, file_path) in enumerate(tqdm(test_data)): # img_path = '/data/dataset/Places365-14/train/kitchen/00000075.jpg'
        batch_img = batch_img.cuda()
        res, _ = model.predict(batch_img)
        temp = as_numpy(res)
        res = as_numpy(torch.argmax(res, axis=1))
        I = entropy(temp,axis=1)
        res_entropy = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
        for _, (res_img, etr_img, path) in enumerate(zip(res, res_entropy, file_path)):
            tail = path.split('/')[-3:]  # tail = ['train', 'kitchen', '00000075.jpg']
            im1 = Image.fromarray(etr_img)
            im1.save(os.path.join(dataset_storepath,'etr',tail[0],tail[1], tail[2]))
            im2 = Image.fromarray(res_img.astype(np.uint8))
            im2.save(os.path.join(dataset_storepath,'res',tail[0],tail[1], tail[2]))
            
            

if __name__ == "__main__":
    map_builder()
    


