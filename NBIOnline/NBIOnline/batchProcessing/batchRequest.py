import json
import threading

from bson import ObjectId
from django.http import HttpResponse

from .batchImageProcess import batchImagePreProcessing
from .compressProcess import getCompressedFiles
from ..dataManagement.dbFunction import getBatchStatusByID, getOriginImage
from ..dataManagement.db_batchProcess import batchProcess
from ..userManagement.token import tokenCheck


# 上传压缩包
def batchUpload_compress(request):
    user = str(request.POST.get("uid"))
    token = str(request.POST.get("token"))
    # 检查登录状态
    # print(tokenCheck(user, token), user, token)
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)

    user = user.replace('.', '^')

    # 尝试解压缩
    packageFile = request.FILES.get("package")
    if packageFile is None:
        return HttpResponse(2)

    srcFolderName = getCompressedFiles(str(packageFile), user, packageFile.temporary_file_path(), "./static/Data/Batch")

    newBatchProcess = batchProcess(uid=user, batchName=str(packageFile).split('.')[0])
    newBatchProcess.srcFolderName = srcFolderName

    # 先同步到数据库中
    batchID = newBatchProcess.saveData().inserted_id

    # 开始配对处理检查，同时更新数据库
    preProcessThread = threading.Thread(target=batchImagePreProcessing, args=(batchID, srcFolderName, user))
    preProcessThread.start()

    ret = {
        "batchID": str(batchID),
        "batchName": str(packageFile).split('.')[0],
    }
    ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")


# 根据批次id查询批次处理状态
def getBatchStatus(request):
    user = str(request.POST.get("uid"))
    token = str(request.POST.get("token"))
    # 检查登录状态
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)

    batchID = ObjectId(request.POST.get("batchID"))
    ret = getBatchStatusByID(batchID)
    ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")


# 解压完成并通过检查的压缩包返回成组信息
def getInitImageInfo(request):
    user = str(request.POST.get("uid"))
    token = str(request.POST.get("token"))
    # 检查登录状态
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)
    batchID = ObjectId(request.POST.get("batchID"))
    ret = getOriginImage(batchID)
    ret = json.dumps(ret)
    return HttpResponse(ret, content_type="application/json")
