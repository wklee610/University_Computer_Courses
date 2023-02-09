import torch
import torch.nn as nn
from tqdm import tqdm
from torchvision.utils import save_image

from utils import data_loader, create_path

class low_pass_filter_mask(nn.Module):
    
    '''
        The input should be two img
        one for entropy map
        the other for semantic map
        first to the entropy map low pass filter
        than we do the samantic map masking
    '''
    
    def __init__(self) -> None:
        super().__init__()
        self.bn = nn.BatchNorm2d(1)
    
    def forward(self, etr_map:torch.Tensor(), sem_map):
        new_etr = fft_low_pass_filter(etr_map, 32, 0.5)
        new_etr = torch.reshape(new_etr, (new_etr.shape[0],1,new_etr.shape[1],new_etr.shape[2])).cuda()
        new_etr = -self.bn(new_etr) # stdardlize it to N(0,1)
        new_etr = torch.squeeze(new_etr)
        new_etr = (new_etr>=0).float()
        sem_map = torch.squeeze(sem_map)+1
        sem_map = sem_map.mul(new_etr)-1
        return sem_map # 0 means you cannot trust this, ood set, others means some classes 
    
        

def low_pass_filter(rate : float, shape: int) ->  torch.Tensor:
    '''
        rate is a float number from 0 to 1, which control how much inforamtion 
        user wants to reserve
        shape is the size of the output 
        image need to be first resize to a w*w size
    '''
    length = (rate*shape/2)
    filter = torch.zeros((shape, shape)).cuda()
    
    for i in range(shape):
        for j in range(shape):
            if (shape/2-i)*(shape/2-i)+(shape/2-j)*(shape/2-j)<length*length:
                filter[i][j] = 1
    return filter

def fft_low_pass_filter(batch_img, shape, rate)->torch.Tensor:
    '''
        we expected a normalized
    '''
    batch_img = torch.squeeze(batch_img)
    lpf = low_pass_filter(rate,shape*2)
    padding_pic = torch.zeros((len(batch_img), shape*2,shape*2)).cuda()
    padding_pic[:, :shape,:shape] = batch_img[:, :shape, :shape]
    fft_result = torch.fft.fft2(padding_pic)
    fft_shift_result = torch.fft.fftshift(fft_result)
    fft_shift_result *= lpf
    invert_shift_img = torch.fft.ifftshift(fft_shift_result)
    new_batch_img = torch.real(torch.fft.ifft2(invert_shift_img))[:, :shape,:shape]
    return new_batch_img


def build_filterd_map(dataset = 'train'):
    
    etr_dataset_storepath = f'seg_result/SUN_RGBD/etr/{dataset}'
    res_dataset_storepath = f'seg_result/SUN_RGBD/res/{dataset}'
    
    store_path = 'seg_result/SUN_RGBDENLPF'

    create_path('seg_result/SUN_RGBDENLPF')

    etr_loader, res_loader, classes_dict = data_loader(etr_dataset_storepath, res_dataset_storepath)
    classes_dict = {v: k for k, v in classes_dict.items()}
    lpfm = low_pass_filter_mask()
    lpfm = lpfm.to(device = 'cuda')
    
    for _, ((imgs_etr, _, filePath_etr), (imgs_res, _, filePath_res)) in enumerate((zip(tqdm(etr_loader), res_loader))):
        imgs_etr = imgs_etr.to(device = 'cuda')
        imgs_res = imgs_res.to(device = 'cuda')
        res = lpfm(imgs_etr, imgs_res)
        for _, (img, path) in enumerate(zip(res, filePath_etr)):
            path = path.split('/')
            path = path[4:]
            path = store_path +f'/{dataset}/'+'/'.join(path)
            save_image(img,path)