import torch
import torch.nn as nn

from config import *
from timm.scheduler.cosine_lr import CosineLRScheduler
from timm.scheduler.step_lr import StepLRScheduler


def my_loss():
    loss = nn.CrossEntropyLoss()
    return loss




def build_scheduler(config, optimizer, n_iter_per_epoch):
    num_steps = int(config.EPOCHS * n_iter_per_epoch)
    warmup_steps = int(config.WARMUP_EPOCHS * n_iter_per_epoch)
    decay_steps = int(config.LR_SCHEDULER_DECAY_EPOCHS * n_iter_per_epoch)

    lr_scheduler = None
    if config.LR_SCHEDULER_NAME == 'cosine':
        lr_scheduler = CosineLRScheduler(
            optimizer,
            t_initial=num_steps,
            lr_min=config.MIN_LR,
            warmup_lr_init=config.WARMUP_LR,
            warmup_t=warmup_steps,
            cycle_limit=2,
            cycle_decay=0.1,
            t_in_epochs=False,
        )
    elif config.LR_SCHEDULER_NAME == 'step':
        lr_scheduler = StepLRScheduler(
            optimizer,
            decay_t=decay_steps,
            decay_rate=config.LR_SCHEDULER_DECAY_RATE,
            warmup_lr_init=config.WARMUP_LR,
            warmup_t=warmup_steps,
            t_in_epochs=False,
        )

    return lr_scheduler


### using the build schedular to train