"""用来处理图片，保存，压缩，转化图片格式的方法"""
import cv2
import rawpy
from .NBIGenerator import getNBIImage_full, getRandom, pillow2cv2, getNBIImage_easy
from PIL import Image as pillowImage

# 输入cv2类图片，直接保存压缩后图片并且在数据库中记录
def compressImage(image, name, rate):
    cname = name.split("_")[0]+"_compress_"+name.split("_")[1]
    # 本来就不大的图片就不压缩
    if image.size > 500000:
        cv2.imwrite(r"../static/Data/Temp/{name}".format(name=cname), image, [cv2.IMWRITE_JPEG_QUALITY, rate])
    else: 
        cv2.imwrite(r"../static/Data/Temp/{name}".format(name=cname), image)
    return cname

def storeInputImage(image_blue, image_green):
    # 将非jpg格式的数据转换成jpg存储
    # jpg格式压缩存储
    if str(image_blue).split(".")[-1].lower() == "jpg" or str(image_blue).split(".")[-1].lower() == "jpeg": 
        image_blue_name = str(image_blue).split(".")[0]+getRandom()+'.jpg'
        image_blue = pillow2cv2(pillowImage.open(image_blue))
        if image_blue.size>500000:
            # 太大的图片略微压缩
            cv2.imwrite(r"../static/Data/Blue/{name}".format(name=image_blue_name), image_blue, [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            # 不大的就几乎不压缩
            cv2.imwrite(r"../static/Data/Blue/{name}".format(name=image_blue_name), image_blue, [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        # 转换为Jpg格式再存储
        image_blue_name = str(image_blue).split(".")[0]+getRandom()+'.jpg'     
        raw2jpg(image_blue, "Blue", image_blue_name)

    if str(image_green).split(".")[-1].lower() == "jpg"  or str(image_blue).split(".")[-1].lower() == "jpeg": 
        image_green_name = str(image_green).split(".")[0]+getRandom()+'.jpg'
        image_green = pillow2cv2(pillowImage.open(image_green))
        if image_green.size>500000:
            cv2.imwrite(r"../static/Data/Green/{name}".format(name=image_green_name), image_green, [cv2.IMWRITE_JPEG_QUALITY, 60])
        else:
            cv2.imwrite(r"../static/Data/Green/{name}".format(name=image_green_name), image_green, [cv2.IMWRITE_JPEG_QUALITY, 80])
    else:
        image_green_name = str(image_green).split(".")[0]+getRandom()+'.jpg' 
        raw2jpg(image_green, "Green", image_green_name)  
    return image_blue_name, image_green_name

# 处理并生成NBI图片
def generateNBIImage_easy(image_blue_name, image_green_name, user, channelOffset, brightnessOffset, isAutoChannel, isAutoBrightness):
    image_blue = pillowImage.open(r"../static/Data/Blue/{name}".format(name=image_blue_name))
    image_green = pillowImage.open(r"../static/Data/Green/{name}".format(name=image_green_name))
    # 临时文件名，加上随机避免前端因为缓存而不更新图片
    resultName = "result_{uid}{rand}.jpg".format(uid=user,rand=getRandom())
    resultImage = None
    try:
        # 输入cv2图片，生成一个cv2类型的图片，存储到指定位置
        resultImage = getNBIImage_easy(
            image_blue=image_blue,
            image_green=image_green,
            isAutoCutImage=True, # TODO
            isAutoChannel=isAutoChannel,
            isAutoBrightness=isAutoBrightness,
            ChannelOffset=channelOffset,
            BrightnessOffset=brightnessOffset,
        )
        cv2.imwrite(r"../static/Data/NBI/{name}".format(name=resultName), resultImage)
    except Exception as e:
        # 返回0表示图片处理过程中出现问题
        print(e)
        return False, resultName, resultImage
    return True, resultName, resultImage

def generateNBIImage_full(image_blue_name, image_green_name, user, channelOffset, brightnessOffset, isAutoChannel, isAutoBrightness, contrast, numinosity, saturation):
    image_blue = pillowImage.open(r"../static/Data/Blue/{name}".format(name=image_blue_name))
    image_green = pillowImage.open(r"../static/Data/Green/{name}".format(name=image_green_name))
    # 临时文件名，加上随机避免前端因为缓存而不更新图片
    resultName = "result_{uid}{rand}.jpg".format(uid=user,rand=getRandom())
    resultImage = None
    try:
        # 输入cv2图片，生成一个cv2类型的图片，存储到指定位置
        resultImage = getNBIImage_full(
            image_blue=image_blue,
            image_green=image_green,
            isAutoCutImage=True, # TODO
            isAutoChannel=isAutoChannel,
            isAutoBrightness=isAutoBrightness,
            ChannelOffset=channelOffset,
            BrightnessOffset=brightnessOffset,
            contrast=contrast,
            numinosity=numinosity,
            saturation=saturation,
        )
        cv2.imwrite(r"../static/Data/NBI/{name}".format(name=resultName), resultImage)
    except Exception as e:
        # 返回0表示图片处理过程中出现问题
        print(e)
        return False, resultName, resultImage
    return True, resultName, resultImage

# 将RAW格式的输入数据转化为jpg储存
def raw2jpg(image, imageType, name):
    rawImage = rawpy.imread(image.temporary_file_path())
    thumb = rawImage.extract_thumb()
    savePath = ""
    if thumb.format == rawpy.ThumbFormat.JPEG:
        if imageType == "Blue":
            savePath = "../static/Data/Blue/"+name
        elif imageType == "Green":
            savePath = "../static/Data/Green/"+name
        with open(savePath, 'wb') as f:
            f.write(thumb.data)