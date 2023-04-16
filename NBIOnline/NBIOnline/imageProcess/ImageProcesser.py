"""用来处理图片，保存，压缩，转化图片格式的方法"""
import time

import cv2
import rawpy
from PIL import Image as pillowImage
from .NBIGenerator import getNBIImage_full, getRandom, pillow2cv2, getNBIImage_easy, getNBIImage_auto
from ..configLoader import nbi_conf
from ..dataManagement.dbFunction import getInfoByUIDAndGID, deleteOneImage
from ..dataManagement.db_ImageData import updateImageData

conf = nbi_conf


# 输入cv2类图片，直接保存压缩后图片并且在数据库中记录
def compressImage(image, name, rate):
    cname = name.split("_")[0] + "_compress_" + name.split("_")[1]
    # 本来就不大的图片就不压缩
    if image.size > conf.configs['image_temp_compress_threshold']:
        cv2.imwrite(r"../NBIOnline/static/Data/Temp/{name}".format(name=cname), image, [cv2.IMWRITE_JPEG_QUALITY, rate])
    else:
        cv2.imwrite(r"../NBIOnline/static/Data/Temp/{name}".format(name=cname), image)
    return cname


# 输入django传过来的temp文件，处理并存储
def storeInputImage(image_blue, image_green, image_white):
    # 将非jpg格式的数据转换成jpg存储
    # jpg格式压缩存储
    if str(image_blue).split(".")[-1].lower() == "jpg" or str(image_blue).split(".")[-1].lower() == "jpeg":
        image_blue_name = str(image_blue).split(".")[0] + getRandom() + '.jpg'
        image_blue = pillow2cv2(pillowImage.open(image_blue))
        if image_blue.size > conf.configs['image_storage_compress_threshold']:
            # 太大的图片略微压缩
            cv2.imwrite(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name), image_blue,
                        [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            # 不大的就几乎不压缩
            cv2.imwrite(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name), image_blue,
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        # 转换为Jpg格式再存储
        image_blue_name = str(image_blue).split(".")[0] + getRandom() + '.jpg'
        raw2jpg(image_blue, "Blue", image_blue_name)

    if str(image_green).split(".")[-1].lower() == "jpg" or str(image_blue).split(".")[-1].lower() == "jpeg":
        image_green_name = str(image_green).split(".")[0] + getRandom() + '.jpg'
        image_green = pillow2cv2(pillowImage.open(image_green))
        if image_green.size > conf.configs['image_storage_compress_threshold']:
            cv2.imwrite(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name), image_green,
                        [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            cv2.imwrite(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name), image_green,
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        image_green_name = str(image_green).split(".")[0] + getRandom() + '.jpg'
        raw2jpg(image_green, "Green", image_green_name)

    if image_white is None:
        image_white_name = None
    else:
        if str(image_white).split(".")[-1].lower() == "jpg" or str(image_white).split(".")[-1].lower() == "jpeg":
            image_white_name = str(image_white).split(".")[0] + getRandom() + '.jpg'
            image_white = pillow2cv2(pillowImage.open(image_white))
            if image_white.size > conf.configs['image_storage_compress_threshold']:
                cv2.imwrite(r"../NBIOnline/static/Data/White/{name}".format(name=image_white_name), image_white,
                            [cv2.IMWRITE_JPEG_QUALITY, 60])
            else:
                cv2.imwrite(r"../NBIOnline/static/Data/White/{name}".format(name=image_white_name), image_white,
                            [cv2.IMWRITE_JPEG_QUALITY, 80])
        else:
            image_white_name = str(image_white).split(".")[0] + getRandom() + '.jpg'
            raw2jpg(image_white, "Green", image_white_name)

    return image_blue_name, image_green_name, image_white_name


# 直接指定图片路径，处理并储存到相应路径下
# 这个函数在解压缩的检查之后被调用
def transPackageImage(image_blue, image_green, image_white):
    # print(image_green, image_blue)
    # 将非jpg格式的数据转换成jpg存储
    # jpg格式压缩存储
    if str(image_blue).split(".")[-1].lower() == "jpg" or str(image_blue).split(".")[-1].lower() == "jpeg":
        image_blue_name = str(image_blue.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
        image_blue = pillow2cv2(pillowImage.open(image_blue))
        if image_blue.size > conf.configs['image_storage_compress_threshold']:
            # 太大的图片略微压缩
            cv2.imwrite(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name), image_blue,
                        [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            # 不大的就几乎不压缩
            cv2.imwrite(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name), image_blue,
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        # 转换为Jpg格式再存储
        image_blue_name = str(image_blue.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
        raw2jpg_file(image_blue, "Blue", image_blue_name)

    if str(image_green).split(".")[-1].lower() == "jpg" or str(image_blue).split(".")[-1].lower() == "jpeg":
        image_green_name = str(image_green.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
        image_green = pillow2cv2(pillowImage.open(image_green))
        if image_green.size > conf.configs['image_storage_compress_threshold']:
            cv2.imwrite(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name), image_green,
                        [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            cv2.imwrite(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name), image_green,
                        [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        image_green_name = str(image_green.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
        raw2jpg_file(image_green, "Green", image_green_name)

    if image_white is None:
        image_white_name = None
    else:
        if str(image_white).split(".")[-1].lower() == "jpg" or str(image_white).split(".")[-1].lower() == "jpeg":
            image_white_name = str(image_white.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
            image_white = pillow2cv2(pillowImage.open(image_white))
            if image_white.size > conf.configs['image_storage_compress_threshold']:
                cv2.imwrite(r"../NBIOnline/static/Data/White/{name}".format(name=image_white_name), image_white,
                            [cv2.IMWRITE_JPEG_QUALITY, 60])
            else:
                cv2.imwrite(r"../NBIOnline/static/Data/White/{name}".format(name=image_white_name), image_white,
                            [cv2.IMWRITE_JPEG_QUALITY, 80])
        else:
            image_white_name = str(image_white.split('/')[-1]).split(".")[0] + getRandom() + '.jpg'
            raw2jpg_file(image_white, "Green", image_white_name)

    return image_blue_name, image_green_name, image_white_name


# 处理并生成NBI图片
def generateNBIImage_easy(image_blue_name, image_green_name, user, channelOffset, brightnessOffset, isAutoChannel,
                          isAutoBrightness):
    image_blue = pillowImage.open(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name))
    image_green = pillowImage.open(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name))
    # 临时文件名，加上随机避免前端因为缓存而不更新图片
    resultName = "result_{uid}{rand}.jpg".format(uid=user, rand=getRandom())
    resultImage = None
    try:
        # 输入cv2图片，生成一个cv2类型的图片，存储到指定位置
        resultImage, brightnessAdjustValue = getNBIImage_easy(
            image_blue=image_blue,
            image_green=image_green,
            isAutoCutImage=True,  # TODO
            isAutoChannel=isAutoChannel,
            isAutoBrightness=isAutoBrightness,
            ChannelOffset=channelOffset,
            BrightnessOffset=brightnessOffset,
        )
        cv2.imwrite(r"../NBIOnline/static/Data/NBI/{name}".format(name=resultName), resultImage)
    except Exception as e:
        # 返回0表示图片处理过程中出现问题
        print(e)
        return False, resultName, resultImage, None
    return True, resultName, resultImage, brightnessAdjustValue


def generateNBIImage_full(image_blue_name, image_green_name, user, channelOffset, brightnessOffset, isAutoChannel,
                          isAutoBrightness, contrast, luminosity, saturation):
    image_blue = pillowImage.open(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name))
    image_green = pillowImage.open(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name))
    # 临时文件名，加上随机避免前端因为缓存而不更新图片
    resultName = "result_{uid}{rand}.jpg".format(uid=user, rand=getRandom())
    resultImage = None
    try:
        # 输入cv2图片，生成一个cv2类型的图片，存储到指定位置
        resultImage, brightnessAdjustValue = getNBIImage_full(
            image_blue=image_blue,
            image_green=image_green,
            isAutoCutImage=True,  # TODO
            isAutoChannel=isAutoChannel,
            isAutoBrightness=isAutoBrightness,
            ChannelOffset=channelOffset,
            BrightnessOffset=brightnessOffset,
            contrast=contrast,
            luminosity=luminosity,
            saturation=saturation,
        )
        cv2.imwrite(r"../NBIOnline/static/Data/NBI/{name}".format(name=resultName), resultImage)
    except Exception as e:
        # 返回0表示图片处理过程中出现问题
        print(e)
        return False, resultName, resultImage, None
    return True, resultName, resultImage, brightnessAdjustValue


def generateNBIImage_auto(image_blue_name, image_green_name, user, channelOffset, brightnessOffset):
    image_blue = pillowImage.open(r"../NBIOnline/static/Data/Blue/{name}".format(name=image_blue_name))
    image_green = pillowImage.open(r"../NBIOnline/static/Data/Green/{name}".format(name=image_green_name))
    # 临时文件名，加上随机避免前端因为缓存而不更新图片
    resultName = "result_{uid}{rand}.jpg".format(uid=user, rand=getRandom())
    resultImage = None
    try:
        # 输入cv2图片，生成一个cv2类型的图片，存储到指定位置
        resultImage, brightnessAdjustValue = getNBIImage_auto(
            image_blue=image_blue,
            image_green=image_green,
            isAutoCutImage=True,  # TODO
            ChannelOffset=channelOffset,
            BrightnessOffset=brightnessOffset,
        )
        cv2.imwrite(r"../NBIOnline/static/Data/NBI/{name}".format(name=resultName), resultImage)
    except Exception as e:
        # 返回0表示图片处理过程中出现问题
        print(e)
        return False, resultName, resultImage, None
    return True, resultName, resultImage, brightnessAdjustValue


# 将RAW格式的输入数据转化为jpg储存
def raw2jpg(image, imageType, name):
    rawImage = rawpy.imread(image.temporary_file_path())
    thumb = rawImage.extract_thumb()
    savePath = ""
    if thumb.format == rawpy.ThumbFormat.JPEG:
        if imageType == "Blue":
            savePath = "../NBIOnline/static/Data/Blue/" + name
        elif imageType == "Green":
            savePath = "../NBIOnline/static/Data/Green/" + name
        with open(savePath, 'wb') as f:
            f.write(thumb.data)


def raw2jpg_file(image, imageType, name):
    rawImage = rawpy.imread(image)
    thumb = rawImage.extract_thumb()
    savePath = ""
    if thumb.format == rawpy.ThumbFormat.JPEG:
        if imageType == "Blue":
            savePath = "../NBIOnline/static/Data/Blue/" + name
        elif imageType == "Green":
            savePath = "../NBIOnline/static/Data/Green/" + name
        with open(savePath, 'wb') as f:
            f.write(thumb.data)


def processImageByID(uid, _id):
    # 因为uid中存在符号.
    # 在进行图片的处理中应当替换掉
    uid = uid.replace(".", "^")

    # 通过数据库找到gid的图片信息
    imgInfo = getInfoByUIDAndGID(uid, _id)

    processResult, resultName, resultImage, _ = generateNBIImage_easy(
        image_blue_name=imgInfo.get("Image_Blue"),
        image_green_name=imgInfo.get("Image_Green"),
        user=uid,
        channelOffset=0,
        brightnessOffset=0,
        isAutoChannel=0,
        isAutoBrightness=0,
    )
    cname = compressImage(resultImage, resultName, 15)

    # 把旧的NBI&&Temp图片删除
    if imgInfo.get("Image_Result") is not None:
        deleteOneImage("NBI", imgInfo.get("Image_Result"))
        deleteOneImage("Temp", imgInfo.get("Image_Compress"))

    # 更新数据库
    updateDict = {
        "Image_Result": resultName,
        "Image_Compress": cname,
        "lastChangeTime": time.time(),
    }

    # 高级用户保存一年，批处理是高级用户的权限，都是保留一年
    if not imgInfo.get("isGenerated"):
        updateDict['expireTime'] = imgInfo.get("expireTime") + 24 * 60 * 60 * 366
        updateDict['isGenerated'] = True

    updateImageData(imgInfo.get("_id"), updateDict)