# -*- coding: utf-8 -*-
"""main_fer2013.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k6-cn2J7ywrBL9YCCVTj3Mr9p0tlc7MI
"""

# gpu_info = !nvidia-smi
# gpu_info = '\n'.join(gpu_info)
# if gpu_info.find('failed') >= 0:
#   print('Not connected to a GPU')
# else:
#   print(gpu_info)

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/WorkSpace/AI_Research/EmotionTorch/code/

# !pip install wandb -qqq
# !pip install pytorchcv -q

import os
import json
import random
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import imgaug
import torch
import torch.multiprocessing as mp
import numpy as np


seed = 1234
random.seed(seed)
imgaug.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
np.random.seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

from utils.datasets.fer2013_ds import FERDataset
# from models.vgg16_cbam import  VGG19_CBAM
from models.resnet_cbam import ResidualNet , cbam_resnet50
from models.vggnet import vgg16_bn, vgg19, vgg19_bn, vgg16
from models.resnet import resnet50
from models.vggnet_cbam import vgg16_cbam, vgg19_cbam
from models.vggnet_cbam_pre import vgg16_cbam_pre, vgg16_bn_cbam_pre, vgg19_bn_cbam_pre, MultiFCVGGnetCBam
from models.test_cbam import TestModel
from models.resmasking import *
from models.BamNetwork import *
from models.New_model import *
from models.ResNetVDSR import resnetvdsr_dropout1

from utils.visualize.show_img import show_image_dataset
from trainer.fer2013_trainer import FER2013_Trainer

print(torch.__version__)

config_path = "./kaggle_Research/configs/config_fer2013.json"

configs = json.load(open(config_path))

train_loader = FERDataset( "train", configs)
val_loader = FERDataset("val", configs)
test_loader_ttau = FERDataset("test", configs, ttau = True, len_tta = 64) 
test_loader = FERDataset("test", configs, ttau = False, len_tta = 48)

# show_image_dataset(train_ds)

# model = resnet50_cbam()
# if torch.cuda.is_available():
#     model.cuda()

# n_inputs = model.classifier[6].in_features  
# model.classifier[6] = nn.Sequential(
#             nn.Linear(n_inputs, 256), nn.ReLU(), nn.Dropout(0.2),
#             nn.Linear(256, 7))

# import torchvision
# model1 = vgg16_bn()
# model = resnet50(True, True, num_classes = 7)
# model1 = ResidualNet("ImageNet", 50, 7, "CBAM")
# model = cbam_resnet50(in_channels=3, num_classes= 7 )
# model = vgg19()
# model = vgg19_bn()
# model1 = vgg16_bn(pretrained = True, batch_norm = True)
# model = vgg19_cbam(num_classes = 7)
# model = vgg16_bn_cbam_pre(num_classes=7)
# pretrained_model = torchvision.models.vgg16_bn(pretrained=True)
# model = TestModel(pretrained_model)
# model = MultiFCVGGnetCBam(model1)
# model = resmasking_dropout1()
# model = resnetvdsr_dropout1()
model = MyModel_dropout1()
# state = torch.load("/content/drive/MyDrive/WorkSpace/AI_Research/EmotionTorch/checkpoints/Fer2013_trainers_V5_test_model22_2022Oct24_02.19")
      
# model.load_state_dict(state["net"])

trainer = FER2013_Trainer(model, train_loader, val_loader, test_loader, test_loader_ttau, configs , wb = True)

# trainer.acc_on_test()
# trainer.acc_on_test_ttau()

if configs["distributed"] == 1:
    ngpus = torch.cuda.device_count()
    print(ngpus)
    mp.spawn(trainer.Train_model, nprocs=ngpus, args=())
else:
    trainer.Train_model()

