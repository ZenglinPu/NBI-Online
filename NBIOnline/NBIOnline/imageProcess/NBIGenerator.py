import math
import random

import cv2
import numpy as np
from PIL import Image

from ..IAT_enhance.autoEnhancer import autoImageUpdater


# get NBI Image
def getNBIImage_easy(image_blue, image_green, isAutoCutImage=True, isAutoBrightness=False, isAutoChannel=False,
                     ChannelOffset=0, BrightnessOffset=0):
    print("Input Image Size:\n\tBlue Image:{b}\n\tGreen Image:{g}".format(b=image_blue.size, g=image_green.size))
    if not image_blue.size == image_green.size:
        print("The Image Size Should be the same")
        if isAutoCutImage:
            print("Auto Cute Image to Same Size.")
            # 自动裁剪
            image_blue, image_green = autoCutImage(image_blue, image_green)
        else:
            return

    image_blue = pillow2cv2(image_blue)
    image_green = pillow2cv2(image_green)

    # 得到灰度图片
    gray_blue, gray_green = getGrayImage(image_blue, image_green)

    # 都是先自动调整，再将输入作为offset进行微调
    # TODO：自动调整通道强度
    if isAutoChannel:
        pass

    # 根据输入再次调整通道
    gray_blue = updateBrightness(gray_blue, ChannelOffset)
    gray_green = updateBrightness(gray_green, -1 * ChannelOffset)

    # 融合通道
    # r来自绿色灰度，g和b来自蓝色灰度
    # merge 是按照BGR格式合并
    mergeImage = cv2.merge([gray_blue, gray_blue, gray_green])

    # 输出前自动调整图片整体亮度以便于观测
    # 自动调整亮度和滑块是互斥操作，同时只会有一种处理方式生效
    if isAutoBrightness:
        mergeImage, brightnessAdjustValue = aug(mergeImage)
    else:
        # 根据输入再次调整图片亮度
        mergeImage = updateBrightness(mergeImage, BrightnessOffset)
        brightnessAdjustValue = BrightnessOffset

    print("Get NBI Image Success.")
    return mergeImage, brightnessAdjustValue


def getNBIImage_full(image_blue, image_green, isAutoCutImage=True, isAutoBrightness=False, isAutoChannel=False,
                     ChannelOffset=0, BrightnessOffset=0, contrast=0, luminosity=0, saturation=0):
    print("Input Image Size:\n\tBlue Image:{b}\n\tGreen Image:{g}".format(b=image_blue.size, g=image_green.size))
    if not image_blue.size == image_green.size:
        print("The Image Size Should be the same")
        if isAutoCutImage:
            print("Auto Cute Image to Same Size.")
            # 自动裁剪
            image_blue, image_green = autoCutImage(image_blue, image_green)
        else:
            return

    image_blue = pillow2cv2(image_blue)
    image_green = pillow2cv2(image_green)

    # 得到灰度图片
    gray_blue, gray_green = getGrayImage(image_blue, image_green)

    # 都是先自动调整，再将输入作为offset进行微调
    # TODO：自动调整通道强度
    if isAutoChannel:
        pass

    # 根据输入再次调整通道
    gray_blue = updateBrightness(gray_blue, ChannelOffset)
    gray_green = updateBrightness(gray_green, -1 * ChannelOffset)

    # 融合通道
    # r来自绿色灰度，g和b来自蓝色灰度
    # merge 是按照BGR格式合并
    mergeImage = cv2.merge([gray_blue, gray_blue, gray_green])

    # 输出前自动调整图片整体亮度以便于观测
    if isAutoBrightness:
        mergeImage, brightnessAdjustValue = aug(mergeImage)
        mergeImage = updateImageWithHSV(mergeImage, 0, contrast, luminosity, saturation)
    else:
        # 根据输入调整图片亮度，对比度，明度，饱和度
        mergeImage = updateImageWithHSV(mergeImage, BrightnessOffset, contrast, luminosity, saturation)
        brightnessAdjustValue = BrightnessOffset

    print("Get NBI Image Success.")
    return mergeImage, brightnessAdjustValue


def getNBIImage_auto(image_blue, image_green, isAutoCutImage=True,
                     ChannelOffset=0, BrightnessOffset=0):
    print("Input Image Size:\n\tBlue Image:{b}\n\tGreen Image:{g}".format(b=image_blue.size, g=image_green.size))
    if not image_blue.size == image_green.size:
        print("The Image Size Should be the same")
        if isAutoCutImage:
            print("Auto Cute Image to Same Size.")
            # 自动裁剪
            image_blue, image_green = autoCutImage(image_blue, image_green)
        else:
            return

    image_blue = pillow2cv2(image_blue)
    image_green = pillow2cv2(image_green)

    # 得到灰度图片
    gray_blue, gray_green = getGrayImage(image_blue, image_green)

    # 根据输入再次调整通道
    gray_blue = updateBrightness(gray_blue, ChannelOffset)
    gray_green = updateBrightness(gray_green, -1 * ChannelOffset)

    # 融合通道
    # r来自绿色灰度，g和b来自蓝色灰度
    # merge 是按照BGR格式合并
    mergeImage = cv2.merge([gray_blue, gray_blue, gray_green])

    # 输出前自动调整图片
    try:
        print("#Ready Into AutoUpdater#")
        mergeImage = autoImageUpdater(mergeImage)
        print("#Already Out of AutoUpdater#")
    except Exception as e:
        print(e)
        return None, BrightnessOffset
    # 根据输入再次调整图片亮度
    mergeImage = updateBrightness(mergeImage, BrightnessOffset)
    brightnessAdjustValue = BrightnessOffset

    print("Get NBI Image Success.")
    return mergeImage, brightnessAdjustValue


# 调整图片亮度，对比度，明度，饱和度
def updateImageWithHSV(sourceImage, brightnessOffset, contrast, luminosity, saturation):
    image = sourceImage
    # 调整亮度
    if not brightnessOffset == 0:
        image = updateBrightness(sourceImage, brightnessOffset)

    # 对比度
    contrast = contrast / 100
    h, w, ch = image.shape  # 获取shape的数值，height和width、通道
    # 新建全零图片数组img2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    img2 = np.zeros([h, w, ch], image.dtype)
    image = cv2.addWeighted(image, contrast, img2, 1 - contrast, 0)

    # 明度
    # print(luminosity)
    if luminosity > 100:
        luminosity = 100
    luminosity = luminosity / 100
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    img_hsv[:, :, 2] = luminosity * img_hsv[:, :, 2]

    # 饱和度
    satsaturation = saturation / 100
    img_hsv[:, :, 1] = satsaturation * img_hsv[:, :, 1]
    image = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return image


# 计算灰度图片，并且调整他们的亮度让后面合成的图片不会出现色彩偏移
def getGrayImage(image_blue, image_green, strength=0.4):
    # 转换为灰度图片
    gray_green = cv2.cvtColor(image_green, cv2.COLOR_BGR2GRAY)
    gray_blue = cv2.cvtColor(image_blue, cv2.COLOR_BGR2GRAY)

    # 调整色阶，使色阶更均匀
    out_blue = np.zeros(gray_blue.shape, gray_blue.dtype)
    cv2.normalize(gray_blue, out_blue, 255 * 0.05, 255 * 0.9, cv2.NORM_MINMAX)
    out_green = np.zeros(gray_green.shape, gray_green.dtype)
    cv2.normalize(gray_green, out_green, 255 * 0.05, 255 * 0.9, cv2.NORM_MINMAX)

    # 根据调整后的亮度进一步调整亮度，使得二者亮度一致
    averageBrightness = (getBrightness(out_blue) + getBrightness(out_green)) / 2
    out_blue = updateBrightness(out_blue, strength * (averageBrightness - getBrightness(out_blue)))
    out_green = updateBrightness(out_green, strength * (averageBrightness - getBrightness(out_green)))

    return out_blue, out_green


# 线性调整亮度
def updateBrightness(image, adjust):
    image = np.uint8(np.clip((1.1 * image + adjust), 0, 255))
    return image


# 计算图片亮度,只针对单通道灰度图
def getBrightness(image):
    return cv2.mean(image)[0]


# 计算色阶分位点，⽬的是去掉的直⽅图两头的异常情况
def compute(img, min_percentile, max_percentile):
    """计算分位点，⽬的是去掉的直⽅图两头的异常情况"""
    max_percentile_pixel = np.percentile(img, max_percentile)
    min_percentile_pixel = np.percentile(img, min_percentile)
    return max_percentile_pixel, min_percentile_pixel


# 自动增强图片亮度
def aug(src):
    """图像亮度增强"""
    if src[:, :, 2].mean() > 130:
        return
    # 先计算分位点，去掉像素值中少数异常值，这个分位点可以⾃⼰配置。
    # ⽐如1中直⽅图的红⾊在0到255上都有值，但是实际上像素值主要在0到20内。
    max_percentile_pixel, min_percentile_pixel = compute(src, 0.5, 99.5)
    # 去掉分位值区间之外的值
    src[src >= max_percentile_pixel] = max_percentile_pixel
    src[src <= min_percentile_pixel] = min_percentile_pixel
    # 将分位值区间拉伸到0到255，这⾥取了255*0.05与255*0.9是因为可能会出现像素值溢出的情况，所以最好不要设置为0到255。
    out = np.zeros(src.shape, src.dtype)
    cv2.normalize(src, out, 255 * 0.02, 255 * 0.88, cv2.NORM_MINMAX)
    return out, out.mean() - src.mean()


def autoCutImage(image_blue, image_green):
    minWidth = min(image_blue.size[0], image_green.size[0])
    minHeight = min(image_blue.size[1], image_green.size[1])
    blue_left = math.ceil((image_blue.size[0] - minWidth) / 2)
    green_left = math.ceil((image_green.size[0] - minWidth) / 2)
    blue_top = math.ceil((image_blue.size[1] - minHeight) / 2)
    green_top = math.ceil((image_green.size[1] - minHeight) / 2)
    image_blue = image_blue.crop((blue_left, blue_top, blue_left + minWidth, blue_top + minHeight))
    image_green = image_green.crop((green_left, green_top, green_left + minWidth, green_top + minHeight))
    return image_blue, image_green


# PIL to cv2
def pillow2cv2(image):
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


# cv2 to PIL
def cv22pillow(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# for test
def showChannel(image):
    zeros = np.zeros(image.shape[:2], dtype="uint8")
    B, G, R = cv2.split(image)
    cv2.imshow("DISPLAY BLUE COMPONENT", cv2.merge([B, zeros, zeros]))  # 显示(B,0,0)图像
    cv2.imshow("DISPLAY GREEN COMPONENT", cv2.merge([zeros, G, zeros]))  # 显示(0,G,0)图像
    cv2.imshow("DISPLAY RED COMPONENT", cv2.merge([zeros, zeros, R]))
    cv2.waitKey()


def getRandom(randomlength=8):
    """
  生成一个指定长度的随机字符串，最前方用~符号隔开，因为发现有的图片名称里面很有可能出现_符号
  """
    #   digits="0123456789"
    ascii_letters = "abcdefghigklmnopqrstuvwxyz"
    str_list = [random.choice(ascii_letters) for i in range(randomlength)]
    random_str = '~' + ''.join(str_list)
    return random_str
