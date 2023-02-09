import torch
import torch.nn as nn
import torch.optim as optim

from config import *
from tqdm import trange, tqdm
from eval import eval_model,eval_resnet
from loss_function import build_scheduler
from utils import load_checkpoint, load_four_dataset_sun_rgbd, load_resnet18_backbone

from timm.loss import LabelSmoothingCrossEntropy


def train(loss_function, backbone1:nn.Module, backbone2:nn.Module, classifier:nn.Module, train_original_data, train_semantic_map, test_original_data, test_semanticmap
          , model_store_path = MODEL_STORE_PATH):
    params = list(backbone1.parameters())+list(classifier.parameters())+list(backbone2.parameters())
    optimizer = optim.SGD(params, LEARNING_RATE, momentum=MOMENTUM, weight_decay=WEIGHT_DECAY)

    LR = LR_Params()
    learning_record = []
    lr_scheduler = build_scheduler(LR, optimizer, len(train_original_data))

    best_acc = 0
    for epoch in trange(EPOCHS):
        if epoch < 60:
            for param in backbone1.parameters(): param.requires_grad = False
            for param in backbone2.parameters(): param.requires_grad = False
        else:
            for param in backbone1.parameters(): param.requires_grad = True
            for param in backbone2.parameters(): param.requires_grad = True
        
        average_loss = 0    
        count = 0

        for i, ((input_picture, target), (input_map, target_2)) in (enumerate(zip(tqdm(train_original_data), train_semantic_map))):
            count += 1

            target = target.cuda()
            img = torch.autograd.Variable(input_picture).cuda()
            input_map = input_map.cuda()
            backbone_features = backbone1(img)
            input_map_featurs = backbone2(input_map)*0
            backbone_features = backbone_features.view(backbone_features.size(0), -1) #transform the size to (batchsize, 2048)
            input_map_featurs = input_map_featurs.view(input_map.size(0),-1)
            combined_feature = torch.cat((backbone_features, input_map_featurs), dim=1) 
            logit = classifier(combined_feature)
            
            loss = loss_function(logit, target)
            optimizer.zero_grad()
            lr_scheduler.step_update((epoch*len(train_original_data)+i))
            loss.backward()
            optimizer.step()

            average_loss += loss.detach().cpu()

        average_loss /= count
        learning_record.append(average_loss)
        print(f'the loss is {average_loss}')
        _, _, acc = eval_model(backbone1,backbone2, classifier,test_original_data, test_semanticmap)
        if acc>best_acc:
            best_acc = acc
            torch.save(backbone1, model_store_path+'/backbone1.tar')
            torch.save(backbone2, model_store_path+'/backbone2.tar')
            torch.save(classifier, model_store_path+'/classifier.tar')
        print(f'best_acc update at epochs {epoch}: {best_acc}')
    return 

def train_resnet18(loss_function, model:nn.Module, train_data, test_data):
    params = list(model.parameters())
    optimizer = optim.SGD(params, LEARNING_RATE, momentum=MOMENTUM, weight_decay=WEIGHT_DECAY)

    LR = LR_Params()
    learning_record = []
    lr_scheduler = build_scheduler(LR, optimizer, len(train_data))

    best_acc = 0
    for epoch in trange(EPOCHS):
        print(f'epochs {epoch}: ')
        '''
            Display of the model info
        '''

        # set wether train the backbone or classifier

        average_loss = 0
        count = 0

        

        for i, (input, target) in (enumerate(train_data)):
            count += 1


            target = target.cuda()
            img = torch.autograd.Variable(input).cuda()
            logit = model(img)
            loss = loss_function(logit, target)
            optimizer.zero_grad()
            lr_scheduler.step_update((epoch*len(train_data)+i))
            loss.backward()
            optimizer.step()
            print(loss)
            average_loss += loss.detach().cpu()

        average_loss /= count
        learning_record.append(average_loss)
        print(f'the loss is {average_loss}')
        _, _, acc = eval_resnet(model, test_data)
        if acc>best_acc:
            best_acc = acc
            torch.save(model.module, 'models/resnet18/model.tar')
        print(f'best_acc update at epochs {epoch}: {best_acc}')
        
    return 
if __name__ == '__main__':
    backbone1, _ = load_checkpoint('models/SUN_RGBD_model')
    backbone2 = load_resnet18_backbone()
    classifier = nn.Linear(2560,19)
    classifier = nn.DataParallel(classifier).cuda()
    train_ori_data, test_ori_data, train_lpf_data, test_lpf_data = load_four_dataset_sun_rgbd()
    loss = LabelSmoothingCrossEntropy()
    train(loss, backbone1, backbone2, classifier,train_original_data = train_ori_data, test_original_data=test_ori_data, 
          train_semantic_map= train_lpf_data, test_semanticmap=test_lpf_data)
    
