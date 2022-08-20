from datetime import datetime
import json
from tkinter import _GridIndex
from urllib import request
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..UserManagement.token import tokenCheck
from .ImageProcesser import compressImage, generateNBIImage_easy, generateNBIImage_full, storeInputImage
from ..dataManagement.dbFunction import deleteOneImage, getAdditionalInfoBy_id, getInfobyUID, getLastImage
from ..dataManagement.db_ImageData import imageData
from ..dataManagement.db_ImageAdditionInfo import imageAdditionInfo


# 查询并返回上一次提交的图片
@csrf_exempt
def chooseLastImage(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(2)

        # 查询现有图片数据库中是否有名字和uid都一样的数据，如果有则说明这是重复提交
        result = getLastImage(user.replace('.', '*'))
        if not result:
            # 返回1表示没有之前提交的图片
            return HttpResponse(1)
        else:
            addtionalInfo = getAdditionalInfoBy_id(result['_id'])
            # 返回0表示可以提交完整的新图片数据
            # print(addtionalInfo)
            ret = {
                'imageBlue': result['Image_Blue'],
                'imageGreen': result['Image_Green'],
                'imageWhite': result['Image_White'],
                'sampleName': addtionalInfo['sampleName'],
                'remark': addtionalInfo['remark'],
            }
            ret = json.dumps(ret)
            return HttpResponse(ret, content_type='application/json')


# 处理单张提交图片
# 先创建数据库新条目，然后处理图片数据并存储
@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        # 因为uid中存在特殊符号.
        # 在进行图片的处理中应当替换掉
        user = user.replace('.', '*')

        image_blue = request.FILES.get("blueImage")
        image_green = request.FILES.get("greenImage")
        image_white = request.FILES.get("whiteImage")

        # 检查是否为空，若为空则没有选择图片
        if image_green is None or image_blue is None:
            # 返回2表示未选中图片提交
            return HttpResponse(2)

        # 处理并存储图片
        try:
            # 存储一组三张图片数据，返回压缩图路由
            image_blue_name, image_green_name, image_white_name = storeInputImage(image_blue=image_blue, image_green=image_green, image_white=image_white)
        except Exception as e:
            print(e)
            # 3表示图片存储过程错误
            return HttpResponse(3)
        # 数据库记录新图片数据
        newImageData = imageData(
            uid=user,
            image_green=image_green_name,
            image_blue=image_blue_name,
            image_white=image_white_name,
            image_result=None,
            image_compress=None,
            lastChangeTime=datetime.now(),
        )
        gid = newImageData.saveData().inserted_id

        # 数据库记录图片附加信息数据
        newAdditionInfo = imageAdditionInfo(
            gid=gid,
            sampleName=request.POST.get("sampleName"),
            part=request.POST.get("part"),
            remark=request.POST.get("remark"),
            preDiagnosis=request.POST.get("diagnoseBefore"),
        )
        newAdditionInfo.saveNewAdditionalInfo()

        # 向前端返回结果名以及缩略图名
        # 处理流程完成且正常
        ret = {
            'imageBlue': image_blue_name,
            'imageGreen': image_green_name,
            'imageWhite': image_white_name,
        }
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')


# 更新单张图片属性，然后重新生成，重新返回结果
@csrf_exempt
def updateInputAndGetNBI(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)

        # 因为uid中存在符号.
        # 在进行图片的处理中应当替换掉
        user = user.replace('.', '*')

        channelOffset = int(request.POST.get("channelOffset"))
        brightnessOffset = int(request.POST.get("brightnessAdjust"))
        isAutoChannel = request.POST.get("isAutoChannel") == "true"
        isAutoBrightness = request.POST.get("isAutoBrightness") == "true"

        mode = request.POST.get("mode")

        # 通过数据库找到上次刚刚提交的图片信息
        lastInfo = getInfobyUID(user)
        # 生成新NBI图片
        if mode == "easy":
            processResult, resultName, resultImage = generateNBIImage_easy(
                image_blue_name=lastInfo.get("Image_Blue"),
                image_green_name=lastInfo.get("Image_Green"),
                user=user,
                channelOffset=channelOffset,
                brightnessOffset=brightnessOffset,
                isAutoChannel=isAutoChannel,
                isAutoBrightness=isAutoBrightness,
            )
            cname = compressImage(resultImage, resultName, 15)
        elif mode == "full":
            contrastOffset = int(request.POST.get("contrastOffset"))  # 对比度
            luminosityOffset = int(request.POST.get("luminosityOffset"))  # 明度
            saturationOffset = int(request.POST.get("saturationOffset"))  # 饱和度

            processResult, resultName, resultImage = generateNBIImage_full(
                image_blue_name=lastInfo.get("Image_Blue"),
                image_green_name=lastInfo.get("Image_Green"),
                user=user,
                channelOffset=channelOffset,
                brightnessOffset=brightnessOffset,
                isAutoChannel=isAutoChannel,
                isAutoBrightness=isAutoBrightness,
                contrast=contrastOffset,
                numinosity=luminosityOffset,
                saturation=saturationOffset
            )
            cname = compressImage(resultImage, resultName, 20)
        else:
            return HttpResponse(3)

        if not processResult or not cname:
            # 返回3表示图片处理过程中出现问题
            return HttpResponse(3)

        # 把旧的NBI&&Temp图片删除
        if lastInfo.get("Image_Result") is not None:
            deleteOneImage('NBI', lastInfo.get("Image_Result"))
            deleteOneImage('Temp', lastInfo.get("Image_Compress"))

        # 更新数据库
        updateImageData = imageData(uid=user,
                                    image_green=lastInfo.get("Image_Green"),
                                    image_blue=lastInfo.get("Image_Blue"),
                                    image_white=lastInfo.get("Image_White"),
                                    image_result=resultName,
                                    image_compress=cname,
                                    lastChangeTime=datetime.now(),
                                    )
        updateImageData.replaceData()

        # 返回新的图片数据到前端
        ret = {
            'resultImage': resultName,
            'showImage': cname
        }
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')
    else:
        # 请求方式错误
        return HttpResponse(2)
    
    
@csrf_exempt
def HistoryImgInfo(request, GID):
    if request.method == 'POST':
        # user = request.POST.get('user')
        # token = request.POST.get('token')
        # # 检查登录状态
        # if not tokenCheck(user, token):
        #     # 1表示登录状态有问题
        #     return HttpResponse(1)

        # # 因为uid中存在符号.
        # # 在进行图片的处理中应当替换掉
        # user = user.replace('.', '*')

        # channelOffset = int(request.POST.get("channelOffset"))
        # brightnessOffset = int(request.POST.get("brightnessAdjust"))
        # isAutoChannel = request.POST.get("isAutoChannel") == "true"
        # isAutoBrightness = request.POST.get("isAutoBrightness") == "true"
        pass
    elif request.method == 'GET':
        # addtionalInfo = getAdditionalInfoBy_id(GID) 
        # ret = {
        #     'sampleName': addtionalInfo['sampleName'],
        #     'part': addtionalInfo['part'],
        #     'preDiagnosis': addtionalInfo['preDiagnosis'],
        #     'pathologic': addtionalInfo['pathologic'],
        #     'cuttingEdge': addtionalInfo['cuttingEdge'],
        #     'differentiation': addtionalInfo['differentiation'],
        #     'remark': addtionalInfo['remark'],
        # }
        ret = {
            'sampleName': 'bob的胃标本',
            'partName': '胃',
            'preDiagnosis': '肺癌|炎症',
            'pathologic': '肺癌|炎症',
            'cuttingEdge': '1',
            'differentiation': '1|2',
            'remark': '备注123',
        }
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')
    else:
        return HttpResponse(2)
        
       

