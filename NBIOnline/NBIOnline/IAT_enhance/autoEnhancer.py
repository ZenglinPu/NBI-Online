import os 
import torch
import cv2
import argparse
import warnings
import torchvision
import numpy as np
from .utils import PSNR, validation, LossNetwork
from .model.IAT_main import IAT
from torchvision.transforms import Normalize, ToPILImage
import matplotlib.pyplot as plt
from PIL import Image

def autoImageUpdater(img, task='enhance', normalize=False):
    # print("#Into AutoUpdater#")

    # 获取本文件的绝对路径
    abs_file = os.path.abspath(__file__)
    # 找到绝对路径的同级目录
    abs_dir = abs_file[:abs_file.rfind('\\')] if os.name == 'nt' else abs_file[:abs_file.rfind(r'/')]	
    # 构造模型文件的绝对路径
    exposure_pretrain = os.path.join(abs_dir, 'best_Epoch_exposure.pth')
    enhance_pretrain = os.path.join(abs_dir, 'best_Epoch_lol_v1.pth')

    # # Weights path
    # exposure_pretrain = r'best_Epoch_exposure.pth'
    # enhance_pretrain = r'best_Epoch_lol_v1.pth'

    normalize_process = Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

    ## Load Pre-train Weights
    model = IAT().cuda()
    if task == 'exposure':
        model.load_state_dict(torch.load(exposure_pretrain))
    elif task == 'enhance':
        model.load_state_dict(torch.load(enhance_pretrain))
    else:
        warnings.warn('Only could be exposure or enhance')
    model.eval()
    

    # print(img.shape)
    ## Load Image
    img = (np.asarray(cv22pillow(img))/ 255.0)
    # print(img.shape)
    if img.shape[2] == 4:
        img = img[:,:,:3]
    input = torch.from_numpy(img).float().cuda()
    input = input.permute(2,0,1).unsqueeze(0)
    if normalize:    # False
        input = normalize_process(input)

    ## Forward Network
    _, _ ,enhanced_img = model(input)

    # print("#Outta AutoUpdater#")
    # print(enhanced_img.shape)

    # return tensor2cv2(enhanced_img)
    return pillow2cv2(ToPILImage()(torch.squeeze(enhanced_img)))


# Tensor to cv2
def tensor2cv2(image):
    imaArr = image.detach().cpu().numpy()
    print("#Processing T2C#")
    return cv2.cvtColor(imaArr, cv2.COLOR_RGB2BGR)


# PIL to cv2
def pillow2cv2(image):
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


# cv2 to PIL
def cv22pillow(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# parser = argparse.ArgumentParser()
# parser.add_argument('--file_name', type=str, default='demo_imgs/low_demo.jpg')
# parser.add_argument('--normalize', type=bool, default=False)
# parser.add_argument('--task', type=str, default='enhance', help='Choose from exposure or enhance')
# config = parser.parse_args()

# torchvision.utils.save_image(enhanced_img, 'result.png')
