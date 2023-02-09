
import numpy as np

from config import *
from tqdm import tqdm
from utils import sun_rgbd_loader






def eval_model(backbone, classifier,test_data):
    '''
        If you want to save the index to class name dict
        then specify the path name in save_dict_path
    '''

    '''
        the all logit will return a size of dataset_size * classsize
        the target will return 0 - (classize-1) 
        in sequence(alphabetically)
    '''
    backbone.eval()
    classifier.eval()


    all_target = []
    all_logit = []
    count = 0
    for i, (input, target) in (enumerate(tqdm(test_data))):
        print()
        
        target = target
        img = input.cuda()
        #img = torch.autograd.Variable(input).cuda()
        backbone_features = backbone(img)
        backbone_features = backbone_features.view(backbone_features.size(0), -1) #transform the size to (batchsize, 2048)
        logit = classifier(backbone_features)
        if (len(all_logit)) == 0:
            all_logit = logit.detach().cpu().numpy()
            all_target = target.detach().cpu().numpy()
        else:
            all_logit = np.concatenate((all_logit, logit.detach().cpu().numpy()), axis=0)
            all_target = np.concatenate((all_target, target.detach().cpu().numpy()), axis=0)
        count += BATCHSIZE
    
    acc = np.sum(np.argmax(all_logit, axis=1) == all_target)/len(all_target)
    print(f'acc: {acc}')
    return all_target, all_logit, acc


def save_logits_file(backbone, classifier,save_path):
    dataset = DATASET_LIST
 
    for i,name in enumerate(dataset):
        loader = sun_rgbd_loader(f'/data/dataset/{name}', False,batchsize=32,number_worker=4)
        target,logit, _ = eval_model(backbone,classifier,loader)
        np.save(f'{save_path}/{name}_target.npy', target)
        np.save(f'{save_path}/{name}_logit.npy', logit)   
        if i == 0:
            loader = sun_rgbd_loader(f'/data/dataset/{name}', True,batchsize=32,number_worker=4)    
            target,logit, _ = eval_model(backbone,classifier,loader)    
            np.save(f'{save_path}/{name}_base_target.npy', target)                    
            np.save(f'{save_path}/{name}_base_logit.npy', logit)                


import numpy as np
import pandas as pd

from sklearn import metrics
from scipy.special import softmax
from scipy.stats import entropy
from config import *


class ood():
    def __init__(self, target:np.ndarray, logits:np.ndarray, fpr_rate:float=0.95, temprature:float = 1.0) -> None:
        self.target = target
        self.logits = logits
        #self.classes_name = classes_name
        self.fpr_rate = fpr_rate
        self.temprature = temprature
        self.prototype = self._get_prototype_distribution()
        self.mean, self.var = self._get_mean_var()
        
    
    def _get_prototype_distribution(self):
        prototype_logit = []
        df_logit = pd.DataFrame(self.logits, columns=[i for i in range(len(self.logits[0]))])
        df_target = pd.DataFrame(self.target, columns=[0])
        for i in range(len(self.logits[0])):
            in_distribution = df_logit.loc[df_target[0] == i]
            in_distribution = in_distribution.loc[in_distribution.max(axis=1) == in_distribution[i]]
            prototype_logit.append(in_distribution.mean())
        prototype_logit = np.array(prototype_logit)
        return prototype_logit*self.temprature
        
    def _get_mean_var(self):
        mean = []
        var = []
        df_logit = pd.DataFrame(self.logits, columns=[i for i in range(len(self.logits[0]))])
        df_target = pd.DataFrame(self.target, columns=[0])
        for i in range(len(self.logits[0])):
            in_distribution = df_logit.loc[df_target[0] == i]
            in_distribution = in_distribution.loc[in_distribution.max(axis=1) == in_distribution[i]]
            mean.append(in_distribution[i].mean())
            var.append(in_distribution[i].var())
        return mean, var
    
    def _get_ood_label(self, target:np.ndarray, in_distribution_classes: list):
        ood_judge = []
        '''
            transform a target np.ndarray to binary classes
            in-distribution or out-distribution
            0                |                1
        '''
        for i in range(len(target)):
            if target[i] in in_distribution_classes :
                ood_judge.append(0)
            else:
                ood_judge.append(1)

        ood_judge = np.array(ood_judge)
        return ood_judge
    
    def _get_roc_result(self, judgement, classes, if_print = False) -> list:
        fpr, tpr, _ = metrics.roc_curve(judgement, classes)
        fpr_at_rate = fpr[tpr >= self.fpr_rate][0]
        error_rate = np.min(0.5 * (1 - tpr) + 0.5 * fpr)
        auc = metrics.auc(fpr, tpr)
        if if_print:
            print(f'FPR @{self.fpr_rate}TPR:', fpr_at_rate)
            print('Detection Error:', error_rate)
            print('AUC: ', auc)
        return [fpr_at_rate, error_rate, auc]
    
    def _standardize(self, logits:np.ndarray):
        std_result = np.zeros(logits.shape)
        for i in range(len(self.mean)):
            std_result[:, i] =  (logits[:, i]- self.mean[i])/self.var[i]
        return std_result
    
    def _get_relative_entropy(self,logits:np.ndarray, target:np.ndarray):
        df_logit = pd.DataFrame(logits*self.temprature,columns=[i for i in range(len(logits[0]))])
        df_target = pd.DataFrame(target, columns=[0])
        relative_entr = []
        new_target = []
        for i in range(len(logits[0])):
            model_think_answer_is_i = df_logit.loc[df_logit.max(axis=1) == df_logit[i]] 
            new_target.append(df_target.loc[df_logit.max(axis=1) == df_logit[i]])
            relative_entr.append(entropy(softmax(model_think_answer_is_i, axis=1), softmax(self.prototype[i]), axis=1))
    
        return relative_entr, new_target
    
    def _get_kl_result(self, logit, target, in_distribtuion_classes):
        kl_divergence, new_target = self._get_relative_entropy(logit, target)
        kl_divergence = np.concatenate(kl_divergence)
        new_target = np.concatenate(new_target)
        ood_judge = self._get_ood_label(new_target, in_distribtuion_classes)
        return self._get_roc_result(ood_judge,kl_divergence)
    
    def ood_report(self, logits, target, in_distribution_classes = None)->pd.DataFrame:
        ood_judge = []
        if in_distribution_classes!= None:
            ood_judge = self._get_ood_label(target, in_distribution_classes)
        else: 
            ood_judge = np.ones(len(target))

        result = []
        score = np.nan_to_num(np.var(logits,axis=1))
        result.append(['EnLPF (ours)']+self._get_roc_result(np.logical_not(ood_judge),score))#larger means in distribution
        result.append(['max_logit']+self._get_roc_result(np.logical_not(ood_judge),np.max(logits, axis=1)))
        result.append(['std_max_logit']+self._get_roc_result(np.logical_not(ood_judge),np.max(self._standardize(logits), axis=1)))
        result.append(['entropy']+self._get_roc_result(ood_judge, entropy(softmax(logits, axis=1),axis = 1)))
        result.append(['kl-prototype']+self._get_kl_result(logits, target, in_distribution_classes))
        df = pd.DataFrame(result, columns =['method', f'fpr{self.fpr_rate}', 'Detection Error', 'AUC']) 
        print(df)
        return df

def ood_test_display():
    for name in DATASET_LIST:
        if name == 'SUN_RGBD':
            continue
        print(name)
        in_train_logits = np.load('logit/SUN_RGBD_base_logit.npy')
        in_train_targets = np.load('logit/SUN_RGBD_base_target.npy')

        in_test_logits = np.load('logit/SUN_RGBD_logit.npy')
        in_test_targets = np.load('logit/SUN_RGBD_target.npy')

        out_test_logits = np.load(f'logit/{name}_logit.npy')
        out_test_targets = np.load(f'logit/{name}_target.npy')+102

        test_data_logits = np.concatenate([in_test_logits, out_test_logits], axis=0)
        test_data_target = np.concatenate([in_test_targets, out_test_targets], axis=0)


        cifar10_base_ood = ood(in_train_targets,in_train_logits, fpr_rate=0.5, temprature=1)
        df = cifar10_base_ood.ood_report(test_data_logits, test_data_target, [i for i in range(0,101)])

       