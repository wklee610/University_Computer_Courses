# by Bo Miao
import time
import logging
import torch.nn as nn
import torch.nn.parallel
import torch.optim
import torch.utils.data
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from PIL import Image
import os
from torchstat import stat

from seg_predict import seg_predict
from models import *
from seg_functions import *

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
logging.basicConfig(level=logging.DEBUG)
logging.info('current time is {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

class main(object):
    def __init__(self, args):
        self.args = args
        self.best_prec1 = 0
        self.start_epoch = 0
        assert args.arch in ["", "resnet18", "resnet50"], "unsupported architecture"
        assert args.arch or args.obj, "must specify at least one model"
        self.data_dir = args.dataset
        self.classes, self.classes_num = load_classes(args.class_file)
        self.obj = args.obj
        self.attn = args.attn
        self.obj_length = 150 if args.obj else 0

        self.base_model = load_base_model(args.arch)
        self.obj_model = None
        self.obj_matrix_length = 1024
        if args.obj:
            self.obj_model = OPAM_Small_Cat_Double_Module(self.obj_matrix_length, self.obj_length, args.arch)
            logging.info(self.obj_model)
            #stat(self.obj_model, (self.obj_matrix_length, self.obj_length, 1)) if args.attn else stat(self.obj_model, (22500,1,1))
            self.obj_model = self.obj_model.cuda()
        self.classifier = Classifier_Mix(self.classes_num, args.arch) \
            if self.base_model and self.obj_model else Classifier_Single(self.classes_num, args.arch)
        logging.info(self.classifier)
        self.classifier = self.classifier.cuda()
        self.seg_model = seg_predict(root=os.path.join(os.getcwd(), "seg"))
        
        if args.checkpoint: 
            self.base_model, self.obj_model, self.classifier, self.start_epoch, self.best_prec1 = \
                load_checkpoint(args.checkpoint, self.base_model, self.obj_model, self.classifier)
        cudnn.benchmark = True

    def eval_model(self, data_dir):
        self.classifier.eval()
        if self.base_model:
            self.base_model.eval()
        if self.obj_model:
            self.obj_model.eval()

        centre_crop = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

        correct_list = []
        total_list = []
        for class_name in os.listdir(data_dir):
            correct, count, num_obj = 0, 0, 0
            for img_name in os.listdir(os.path.join(data_dir, class_name)):
                img_dir = os.path.join(data_dir, class_name, img_name)
                img = Image.open(img_dir)
                img = centre_crop(img).unsqueeze(0).cuda()
                logit = calculate_logit(img, [img_dir], self.base_model, self.obj_model, self.classifier,
                                        self.obj, self.attn, self.seg_model)
                result = classify_step(logit, self.classes)

                if result == class_name:
                    correct += 1
                count += 1
            acc = 100 * correct / float(count)
            logging.info('Accuracy of {} class is {:2.2f}%, sample number is {}'.format(class_name, acc, count))
            correct_list.append(correct)
            total_list.append(count)
        acc = sum(correct_list) / float(sum(total_list))
        logging.info('Average test accuracy is = {:2.2f}%'.format(100 * acc))

        return acc


    def train_model(self):
        train_data = load_data(os.path.join(self.data_dir, 'train'), self.args, train=True)
        criterion = nn.CrossEntropyLoss().cuda()
        if self.obj_model:
            params = list(self.obj_model.parameters()) + list(self.classifier.parameters())
        else:
            params = list(self.classifier.parameters())
        optimizer = torch.optim.SGD(params, self.args.lr,
                                    momentum=self.args.momentum,
                                    weight_decay=self.args.weight_decay)

        for epoch in range(self.start_epoch, self.args.epochs):
            print('starting epoch {}'.format(int(epoch)+1))
            cur_lr = adjust_learning_rate(optimizer, epoch, self.args.lr)
            abs_ckpt, abs_ckpt_best = def_ckpt_name(self.args.arch, self.obj_length, self.classes_num,
                                                    self.attn, self.data_dir.split('/')[-1], self.args.extra)

            if epoch != 0 and epoch % 5 == 0:
                self.base_model, self.obj_model, self.classifier = \
                    reload_model(self.base_model, self.obj_model, self.classifier, abs_ckpt_best)

            self.classifier.train()
            if self.base_model:
                self.base_model.train()
            if self.obj_model:
                self.obj_model.train()

            batch_time = AverageMeter()
            data_time = AverageMeter()
            losses = AverageMeter()
            top1 = AverageMeter()
            end = time.time()

            for i, (input, target, path) in enumerate(train_data):
                data_time.update(time.time()-end)
                target = target.cuda()
                img = torch.autograd.Variable(input).cuda()
                logit = calculate_logit(img, path, self.base_model, self.obj_model, self.classifier,
                                        self.obj, self.attn, self.seg_model)
                loss = criterion(logit, target)    
                precision = accuracy(logit.data, target, topk=(1,))[0]
                losses.update(loss, input.size(0))
                top1.update(precision, input.size(0))

                # compute gradient and do SGD step
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()
                if i<10 or i % 50 == 0:
                    logging.info('Train: [Epoch: {0}] [Batch {1}/{2}]\t'
                            'Time {batch_time.val:.3f}s (avg: {batch_time.avg:.3f}s)\t'
                          'Data {data_time.val:.3f}s ({data_time.avg:.3f}s)\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'TrainPrec@1 {top1.val:.3f}% ({top1.avg:.3f}%)\t'.format(
                           epoch+1, i+1, len(train_data), batch_time=batch_time,
                           data_time=data_time, loss=losses, top1=top1))

            acc = self.eval_model(os.path.join(self.data_dir, 'val'))
            # remember best prec@1 and save checkpoint
            save_checkpoint({
                'epoch': epoch + 1,
                'arch': self.args.arch,
                'model_state_dict': self.base_model.state_dict() if self.base_model else {},
                'obj_state_dict': self.obj_model.state_dict() if self.obj_model else {},
                'classifier_state_dict': self.classifier.state_dict(),
                'best_prec1': self.best_prec1,
            }, acc,  self.best_prec1, abs_ckpt, abs_ckpt_best, self.base_model, self.obj_model)
            self.best_prec1 = max(acc, self.best_prec1)
            print("The best validation accuracy obtained during training is = {}%, "
                  "current lr = {:.4f}".format(self.best_prec1*100, cur_lr))


if __name__ == "__main__":
    args = default_argument_parser().parse_args()
    print(args)
    entrance = main(args)
    if args.eval_only:
        entrance.eval_model(args.dataset)
    else:
        entrance.train_model()


    # def val_model(self, val_data):
    #     self.classifier.eval()
    #     if self.base_model:
    #         self.base_model.eval()
    #     if self.obj_model:
    #         self.obj_model.eval()

    #     atch_time = AverageMeter()
    #     top1 = AverageMeter()
    #     end = time.time()
    #     sample_counter = 0

    #     for i, (input, target, path) in enumerate(val_data):
    #         target = target.cuda()
    #         x = torch.autograd.Variable(input).cuda()
    #         with torch.no_grad():
    #             if self.base_model:
    #                 backbone_feature = model(x)
    #                 backbone_feature = backbone_feature.view(backbone_feature.size(0), -1)

    #             if self.obj_model:
    #                 t = get_obj_batch_vector(path, self.args.attention, self.one_hot, self.one_hot_num)
    #                 obj_feature = self.obj_model(t)

    #             if self.base_model and self.obj_model:
    #                 logit = self.classifier(backbone_feature, obj_feature)
    #             elif self.obj_model:
    #                 logit = self.classifier(obj_feature)
    #             elif self.base_model:
    #                 logit = self.classifier(backbone_feature)

    #         # measure accuracy and record loss
    #         precision = accuracy(logit.data, target, topk=(1,))[0]
    #         top1.update(precision, input.size(0))
    #         # measure elapsed time
    #         batch_time.update(time.time() - end)
    #         end = time.time()
    #         sample_counter += 1
    #         if i % 10 == 0:
    #             logging.info('Test: [Batch {0}/{1}]\t'
    #                     'Time {batch_time.val:.3f}s (avg: {batch_time.avg:.3f})s\t'
    #                     'Prec@1 {top1.val:.3f}% ({top1.avg:.3f}%)\t'.format(
    #                 i+1, len(val_data), batch_time=batch_time, top1=top1))

    #     logging.info('Finish validate all {} batches, validation precision is {}'
    #       .format(sample_counter, top1.avg))

    #     return top1.avg

# def main(args):
#     best_prec1 = 0
#     assert args.arch in ["", "resnet18", "resnet50"], "unsupported architecture"
#     assert args.arch or args.obj, "must specify a models"
#     use_one_hot = True if args.obj != '' else False
#     use_backbone = True if args.arch != '' else False
#     use_attention = True if args.attention else False

#     classes, num_classes = load_classes(args.class_file)
#     # load backbone models & structure
#     base_model = load_base_model(args.arch)



#     if args.obj:
#         one_hot, one_hot_cls_num = args.obj, 150
#         if args.attention:
#             object_idt = OPAM_Module(512, one_hot_cls_num, args.arch)
#         else:
#             object_idt = COPM_Module(one_hot_cls_num, args.arch)
#         object_idt = torch.nn.DataParallel(object_idt).cuda()
#         print(object_idt)
#     else:
#         one_hot, one_hot_cls_num = None, 0
#         object_idt = None

#     classifier = None
#     if use_backbone and use_one_hot:
#         classifier = Classifier_Mix(num_classes, args.arch)
#         classifier = torch.nn.DataParallel(classifier).cuda()
#     elif (use_backbone and not use_one_hot) or (not use_backbone and use_one_hot):
#         classifier = Classifier_Single(num_classes, args.arch)
#         #classifier = Classifier_Small_Single(num_classes, args.arch)
#         classifier = torch.nn.DataParallel(classifier).cuda()
#     print(classifier)

#     if args.checkpoint: 
#         base_model, object_idt, classifier, args.start_epoch, best_prec1 = \
#             load_checkpoint(args.checkpoint, base_model, object_idt, classifier)
    
#     cudnn.benchmark = True

#     # load data (picture, webcam, video)
#     data_dir = args.dataset
#     # if args.test:
#     #     _test(data_dir, args.test_type, use_one_hot, use_backbone, use_attention,
#     #           base_model, object_idt, classifier, classes, one_hot, one_hot_cls_num)
#     #     return

#     if args.eval_only:
#         _eval(data_dir, use_one_hot, use_backbone, use_attention,
#               base_model, object_idt, classifier, classes, one_hot, one_hot_cls_num)
#         return
    
#     train_data, val_data = get_data(data_dir, args)
#     criterion = nn.CrossEntropyLoss().cuda()
#     if use_one_hot:
#         params = list(object_idt.parameters()) + list(classifier.parameters())
#     else:
#         params = list(classifier.parameters())
#     optimizer = torch.optim.SGD(params, args.lr,
#                                 momentum=args.momentum,
#                                 weight_decay=args.weight_decay)

#     for epoch in range(args.start_epoch, args.epochs):
#         print('starting epoch {}'.format(int(epoch)+1))
#         cur_lr = adjust_learning_rate(optimizer, epoch, args.lr)
#         abs_ckpt, abs_ckpt_best = def_ckpt_name(args.arch, one_hot_cls_num, num_classes, use_attention, data_dir.split('/')[-1], args.extra)
#         print('best checkpoint is {}'.format(abs_ckpt_best))

#         if epoch != 0 and epoch % 10 == 0:
#             base_model, object_idt, classifier = \
#                 reload_model(base_model, classifier, object_idt, abs_ckpt_best)
#         train(train_data, base_model, object_idt, classifier, criterion, optimizer, epoch, use_one_hot, use_backbone, use_attention, one_hot, one_hot_cls_num)
#         prec1 = val(val_data, base_model, object_idt, classifier, use_one_hot, use_backbone, use_attention, one_hot, one_hot_cls_num)

#         # remember best prec@1 and save checkpoint
#         save_checkpoint({
#             'epoch': epoch + 1,
#             'arch': args.arch,
#             'model_state_dict': base_model.state_dict() if use_backbone else {},
#             'obj_state_dict': object_idt.state_dict() if use_one_hot else {},
#             'classifier_state_dict': classifier.state_dict(),
#             'best_prec1': best_prec1,
#         }, prec1,  best_prec1, abs_ckpt, abs_ckpt_best, use_one_hot)
#         best_prec1 = max(prec1, best_prec1)
#         print("The best accuracy obtained during training is = {}, "
#               "current lr = {:.4f}".format(best_prec1, cur_lr))


# if __name__ == '__main__':
#     args = default_argument_parser().parse_args()
#     print(args)
#     main(args)
