from django.http import HttpResponse
from ..userManagement.token import tokenCheck


# 上传压缩包
def batchUpload_compress(request):
    user = str(request.META.get("HTTP_UID"))
    token = str(request.META.get("HTTP_UTOKEN"))
    # 检查登录状态
    print(tokenCheck(user, token),user,token)
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)

    package = request.FILES
    print(package)


# 根据批次id查询批次处理状态
def getBatchStatus(request):
    pass


# 解压完成并通过检查的压缩包返回成组信息
def getInitImageInfo(request):
    pass
