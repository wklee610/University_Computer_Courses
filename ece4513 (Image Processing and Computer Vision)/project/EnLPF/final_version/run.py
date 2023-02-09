
from lpf_combine import build_filterd_map
from utils import load_checkpoint
from eval import save_logits_file, ood_test_display

if __name__ == '__main__':
    '''
        first use map builder to build entropy map and semantic map
    '''
    build_filterd_map()
    build_filterd_map('val')
    backbone, classifier = load_checkpoint('models/SUN_RGBD_model')
    save_logits_file(backbone, classifier, 'logit')
    ood_test_display()
    


        
