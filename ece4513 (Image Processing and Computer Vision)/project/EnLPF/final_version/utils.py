import os
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms

from torchvision.datasets import ImageFolder
from torchvision.models import ResNet18_Weights

class ImageFolderWithPaths(ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method that dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns 
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path



def data_loader(etr_dataset_storepath:str, res_dataset_storepath,batchsize:int = 32, worker_number:int = 2):

    etr_dataset = ImageFolderWithPaths(
        root=etr_dataset_storepath,
        transform= transforms.Compose([
            transforms.Resize((32,32)),
            transforms.Grayscale(),
            transforms.ToTensor(),
        ])
    )
    
    res_dataset = ImageFolderWithPaths(
        root=res_dataset_storepath,
        transform= transforms.Compose([
            transforms.Resize((32,32)),
            transforms.Grayscale(),
            transforms.ToTensor(),
        ])
    )
    
    etr_data_loader = torch.utils.data.DataLoader(
            etr_dataset,
            batch_size = batchsize, shuffle=False,
            num_workers = worker_number, pin_memory=True)
    
    res_data_loader = torch.utils.data.DataLoader(
        res_dataset,
        batch_size = batchsize, shuffle=False,
        num_workers = worker_number, pin_memory=True)
    
    return etr_data_loader, res_data_loader, res_dataset.class_to_idx

def create_path(dataset_storepath:str, path_copy_from:str = '/data/dataset/SUN_RGBD/train'):
    if not os.path.exists(dataset_storepath):
        '''
            create folder path for each classes
        '''
        for name in os.listdir(path_copy_from):
            os.makedirs(os.path.join(dataset_storepath+'/train'+'/'+name)) #since we do not do the training for seg
            os.makedirs(os.path.join(dataset_storepath+'/val'+'/'+name)) #since we do not do the training for seg

def sun_rgbd_loader(store_path:str, train = True, batchsize = 256, number_worker = 16):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    if train:
        dataset = ImageFolder(store_path+'/train', transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(20),
            transforms.ToTensor(),
            normalize,
        ]))
    else: # did we use this method during test?
        dataset = ImageFolder(store_path+'/val', transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            normalize,
        ]))
    

    data_loader = torch.utils.data.DataLoader(
            dataset,
            batch_size = batchsize, shuffle=False,
            num_workers = number_worker, pin_memory=True)
    
    
    return data_loader

def load_checkpoint(checkpoint_path = './model', linear_node_size = 19):
    backbone_state_dict = torch.load(checkpoint_path +'/backbone.tar')
    backbone_state_dict = {str.replace(k, 'module.', ''): v for k, v in backbone_state_dict.items()}
    backbone = models.resnet50(pretrained=None)
    backbone = nn.Sequential(*list(backbone.children())[:-1])
    backbone.load_state_dict(backbone_state_dict)
    backbone = nn.DataParallel(backbone).cuda()
    classifier_state_dict = torch.load(checkpoint_path+'/classifier.tar')
    classifier =  nn.Linear(2048,linear_node_size).cuda()
    classifier_state_dict = {str.replace(k, 'module.', ''): v for k, v in classifier_state_dict.items()}
    classifier.load_state_dict(classifier_state_dict)
    return backbone,classifier

def load_four_dataset_sun_rgbd(original_store_path = '/data/dataset/SUN_RGBD', enlpf_store_path = 'seg_result/SUN_RGBDENLPF'):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ori_train_dataset = ImageFolder(original_store_path+'/train', transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(20),
            transforms.ToTensor(),
            normalize,
        ]))
    
    enlpf_train_dataset = ImageFolder(enlpf_store_path+'/train', transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ToTensor(),
        normalize
    ]))
    
    ori_test_dataset = ImageFolder(original_store_path+'/val', transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            normalize,
        ]))
    enlpf_test_dataset = ImageFolder(enlpf_store_path+'/val', transform = transforms.Compose([    
            transforms.Resize(224),
            transforms.ToTensor(),
            normalize,
        ]))    
    
    ori_train_loader = torch.utils.data.DataLoader(
        ori_train_dataset,
        batch_size = 256, shuffle=False,
        num_workers = 16, pin_memory=True)
    
    ori_test_loader = torch.utils.data.DataLoader(
        ori_test_dataset,
        batch_size = 256, shuffle=False,
        num_workers = 16, pin_memory=True)
    
    enlpf_train_loader = torch.utils.data.DataLoader(
        enlpf_train_dataset,
        batch_size = 256, shuffle=False,
        num_workers = 16, pin_memory=True)
    
    enlpf_test_loader = torch.utils.data.DataLoader(
        enlpf_test_dataset,
        batch_size = 256, shuffle=False,
        num_workers = 16, pin_memory=True)

    return ori_train_loader, ori_test_loader, enlpf_train_loader, enlpf_test_loader
    
    
def load_resnet18():
    model = models.resnet18(weights = ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(512,19)
    return nn.DataParallel(model).cuda()

def load_resnet18_backbone(path = 'models/resnet18/model.tar'):
    model = torch.load(path)
    backbone = nn.Sequential(*list(model.children())[:-1])
    backbone = nn.DataParallel(backbone).cuda()
    return backbone
    
    