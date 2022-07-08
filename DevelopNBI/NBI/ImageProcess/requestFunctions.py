import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from NBI.UserManagement.token import tokenCheck
from .ImageProcesser import compressImage, generateNBIImage_easy, generateNBIImage_full, storeInputImage
from NBI.dataManagement.dbFunction import deleteOneImage, getInfobyUID, getLastImage
from NBI.dataManagement.db_ImageData import imageData

# 查询并返回上一次提交的图片
@csrf_exempt
def chooseLastImage(request):
    if request.method == 'POST':
        user=request.POST.get('user').replace('.','*')
        
        # 查询现有图片数据库中是否有名字和uid都一样的数据，如果有则说明这是重复提交
        result = getLastImage(user)
        if not result:
            # 返回1表示没有之前提交的图片
            return HttpResponse(1)
        else:
            # 返回0表示可以提交完整的新图片数据
            return HttpResponse(result)

# 处理单张提交图片
# 先创建数据库新条目，然后处理图片数据并存储
@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        
        # 因为uid中存在符号.
        # 在进行图片的处理中应当替换掉
        user  = user.replace('.','*')

        image_blue = request.FILES.get("image_blue")
        image_green = request.FILES.get("image_green")
        # image_green.
        # 检查是否为空，若为空则没有选择图片
        if image_green is None or image_blue is None:
            # 返回2表示未选中图片提交
            return HttpResponse(2)

        # 处理并存储图片
        try:
            image_blue_name, image_green_name = storeInputImage(image_blue=image_blue, image_green=image_green)
        except Exception as e:
            print(e)
            # 3表示图片存储过程错误
            return HttpResponse(3)

        # 数据库记录
        newImageData = imageData(
            uid=user, 
            image_green=image_green_name, 
            image_blue=image_blue_name, 
            image_result=None, 
            image_compress=None,
        )
        newImageData.saveData()

        # 向前端返回结果名以及缩略图名
        # 处理流程完成且正常
        ret = {
            'image_blue': image_blue_name,
            'image_green': image_green_name,
        }
        ret = json.dumps(ret)
        return HttpResponse(ret,content_type='application/json')

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
        user  = user.replace('.','*')

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
            cname = compressImage(resultImage, resultName, 20)
        elif mode == "full":
            contrastOffset = int(request.POST.get("contrastOffset")) # 对比度
            numinosityOffset = int(request.POST.get("numinosityOffset")) # 明度
            saturationOffset = int(request.POST.get("saturationOffset")) # 饱和度

            processResult, resultName, resultImage = generateNBIImage_full(
                image_blue_name=lastInfo.get("Image_Blue"),
                image_green_name=lastInfo.get("Image_Green"), 
                user=user,
                channelOffset=channelOffset,
                brightnessOffset=brightnessOffset,
                isAutoChannel=isAutoChannel,
                isAutoBrightness=isAutoBrightness,
                contrast=contrastOffset,
                numinosity=numinosityOffset,
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
            image_result=resultName, 
            image_compress=cname
        )
        updateImageData.replaceData()

        # 返回新的图片数据到前端
        ret = {
            'resultImage': resultName,
            'showImage': cname
        }
        ret = json.dumps(ret)
        return HttpResponse(ret,content_type='application/json')
    else:
        # 请求方式错误
        return HttpResponse(2)
