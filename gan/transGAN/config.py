#   Copyright (c) 2021 PPViT Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration
Configuration for data, model archtecture, and training, etc.
Config can be set by .yaml file or by argparser(limited usage)
"""
import os
from yacs.config import CfgNode as CN
import yaml

_C = CN()
_C.BASE = ['']

_C.DATA = CN()
_C.DATA.BATCH_SIZE = 32 # train batch_size for single GPU
_C.DATA.BATCH_SIZE_EVAL = 8 # val batch_size for single GPU
_C.DATA.DATA_PATH = '/dataset/imagenet/' # path to dataset
_C.DATA.DATASET = 'cifar10' # dataset name
_C.DATA.IMG_SIZE = 32 # input image size
_C.DATA.CROP_PCT = 0.875 # input image scale ratio, scale is applied before centercrop in eval mode
_C.DATA.NUM_WORKERS = 2 # number of data loading threads 
_C.DATA.GEN_BATCH_SIZE = 128 # the batch size of gen
_C.DATA.DIS_BATCH_SIZE = 64
_C.DATA.NUM_EVAL_IMAGES = 2000 # when calculate fid, default is 20000
_C.DATA.DIFF_AUG = "" # when train the dis_net, have to choose the aug method


# model settings
_C.MODEL = CN()
_C.MODEL.RESUME = None
_C.MODEL.PRETRAINED = None
_C.MODEL.NUM_CLASSES = 1000
_C.MODEL.DROPOUT = 0.1

# transformer settings
_C.MODEL.TRANS = CN()
_C.MODEL.GEN_MODEL = "ViT_custom"
_C.MODEL.DIS_MODEL = "ViT_custom_scale2"
_C.MODEL.PATCH_SIZE = 2
_C.MODEL.LATENT_DIM = 256
_C.MODEL.GF_DIM = 1024
_C.MODEL.DF_DIM = 384
_C.MODEL.BOTTOM_WIDTH = 8
_C.MODEL.FAED_IN = 0.0
_C.MODEL.D_DEPTH = 3
_C.MODEL.G_DEPTH = "5,4,2"
_C.MODEL.G_NORM = "ln"
_C.MODEL.D_NORM = "ln"
_C.MODEL.G_ACT = "gelu"
_C.MODEL.D_ACT = "gelu"
_C.MODEL.G_MLP = 4
_C.MODEL.D_MLP = 4
_C.MODEL.D_WINDOW_SIZE = 8

# training settings
_C.TRAIN = CN()
_C.TRAIN.LAST_EPOCH = 0
_C.TRAIN.NUM_EPOCHS = 300
_C.TRAIN.WARMUP_EPOCHS = 3
_C.TRAIN.WEIGHT_DECAY = 0.05
_C.TRAIN.BASE_LR = 0.001
_C.TRAIN.WARMUP_START_LR = 1e-6
_C.TRAIN.END_LR = 5e-4
_C.TRAIN.GRAD_CLIP = 1.0
_C.TRAIN.ACCUM_ITER = 2 #1

_C.TRAIN.LR_SCHEDULER = CN()
_C.TRAIN.LR_SCHEDULER.NAME = 'warmupcosine'

_C.TRAIN.OPTIMIZER = CN()
_C.TRAIN.OPTIMIZER.NAME = 'AdamW'
_C.TRAIN.OPTIMIZER.EPS = 1e-8
_C.TRAIN.OPTIMIZER.BETAS = (0.9, 0.999)  # for adamW
_C.TRAIN.OPTIMIZER.MOMENTUM = 0.9

# misc
_C.SAVE = "./output"
_C.TAG = "default"
_C.SAVE_FREQ = 10 # freq to save chpt
_C.REPORT_FREQ = 100 # freq to logging info
_C.VALIDATE_FREQ = 100 # freq to do validation
_C.SEED = 0
_C.EVAL = False # run evaluation only
_C.LOCAL_RANK = 0
_C.NGPUS = -1
_C.G_LR = 0.0001
_C.WD = 0.001
_C.D_LR = 0.0001
_C.LR_DECAY = False
_C.LOAD_PATH = ""
_C.EVAL_BATCH_SIZE = 8
_C.SHARED_EPOCH = 15
_C.GROW_STEP1 = 15
_C.GROW_STEP2 = 55
_C.MAX_SEARCH_ITER = 90
_C.HID_SIZE = 100
_C.RL_NUM_EVAL_IMG = 5000
_C.NUM_CANDIDATE = 10
_C.ENTROPY_COEFF = 0.001
_C.DYNAMIC_RESET_THRESHOLD = 0.001
_C.DYNAMIC_RESET_WINDOW = 500
_C.ARCH = None
_C.OPTIMIZER = "adam"
_C.LOSS = "wgangp-eps"
_C.PHI = 1.0
_C.GROW_STEPS = [0,0] 
_C.D_DOWNSAMPLE = "avg"
_C.ACCUMULATED_TIMES = 1
_C.G_ACCUMULATED = 1
_C.NUM_LANDMARKS = 64
_C.D_HEADS = 4
_C.DROPOUT = 0.0
_C.EMA = 0.9999
_C.EMA_WARMUP = 0.1
_C.EMA_KIMG = 500
_C.LATENT_NORM = False
_C.MINISTD = False

def _update_config_from_file(config, cfg_file):
    config.defrost()
    with open(cfg_file, 'r') as infile:
        yaml_cfg = yaml.load(infile, Loader=yaml.FullLoader)
    for cfg in yaml_cfg.setdefault('BASE', ['']):
        if cfg:
            _update_config_from_file(
                config, os.path.join(os.path.dirname(cfg_file), cfg)
            )
    print('merging config from {}'.format(cfg_file))
    config.merge_from_file(cfg_file)
    config.freeze()

def update_config(config, args):
    """Update config by ArgumentParser
    Args:
        args: ArgumentParser contains options
    Return:
        config: updated config
    """
    if args.cfg:
        _update_config_from_file(config, args.cfg)
    config.defrost()
    if args.dataset:
        config.DATA.DATASET = args.dataset
    if args.batch_size:
        config.DATA.BATCH_SIZE = args.batch_size
    if args.image_size:
        config.DATA.IMAGE_SIZE = args.image_size
    if args.data_path:
        config.DATA.DATA_PATH = args.data_path
    if args.ngpus:
        config.NGPUS = args.ngpus
    if args.eval:
        config.EVAL = True
        config.DATA.BATCH_SIZE_EVAL = args.batch_size
    if args.pretrained:
        config.MODEL.PRETRAINED = args.pretrained
    if args.resume:
        config.MODEL.RESUME = args.resume
    if args.last_epoch:
        config.MODEL.LAST_EPOCH = args.last_epoch

    #config.freeze()
    return config


def get_config():
    """Return a clone of config"""
    config = _C.clone()
    return config