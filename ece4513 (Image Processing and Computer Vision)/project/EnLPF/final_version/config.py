
# training overall setting
LOAD_MODEL_PATH = 'pretrained_model/resnet50_places365.pth.tar'
BATCHSIZE = 256
EVAL_BACHSIZE = 64
EPOCHS = 160
DATASET = '/data/scene/datasets/MIT67'
BACKBONE_TRAIN = False
CLASSIFIER_TRAIN = True
MODEL_STORE_PATH = 'models/cobined_model'
DATASET_LIST = ['SUN_RGBD','MIT67','Places365-14']

# CIFAR10 specific parameters
BATCHSIZE_CIFAR10 = 196
MODEL_STORE_PATH_CIFAR10 = './models/CIFAR10'

# CIFAR100 specifi parameters
BATCHSIZE_CIFAR100 = 196

# stored model path
# backbone model
# classifier model



# optimizer setting
LEARNING_RATE = 0.01
MOMENTUM = 0.9
WEIGHT_DECAY = 1e-4

# hardware setting
WORKERS_NUMBER = 16

# for utils
IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')

class LR_Params():
    def __init__(self):
        # -----------------------------------------------------------------------------
        # Training settings
        # -----------------------------------------------------------------------------
        self.START_EPOCH = 0
        self.EPOCHS = 40
        self.WARMUP_EPOCHS = 20
        self.WEIGHT_DECAY = 0.3
        self.BASE_LR = 2e-2
        self.WARMUP_LR = 5e-6
        self.MIN_LR = 5e-5
        # Clip gradient norm
        self.CLIP_GRAD = 5.0
        # Auto resume from latest checkpoint
        self.AUTO_RESUME = True
        # Gradient accumulation steps
        # could be overwritten by command line argument
        self.ACCUMULATION_STEPS = 1
        # Whether to use gradient checkpointing to save memory
        # could be overwritten by command line argument
        self.USE_CHECKPOINT = False

        # LR scheduler
        self.LR_SCHEDULER_NAME = 'cosine'
        # Epoch interval to decay LR, used in StepLRScheduler
        self.LR_SCHEDULER_DECAY_EPOCHS = 30
        # LR decay rate, used in StepLRScheduler
        self.LR_SCHEDULER_DECAY_RATE = 0.1

