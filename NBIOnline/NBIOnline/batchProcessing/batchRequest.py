import json
import threading
from tkinter import E

from bson import ObjectId
from django.http import HttpResponse

from .batchImageProcess import batchImagePreProcessing, nbiImageProcessing
from .compressProcess import getCompressedFile_inMemory, getCompressedFiles
from ..dataManagement.dbFunction import getBatchStatusByID, getOriginImage, deleteAllInfoOfImageBy_id
from ..dataManagement.db_batchProcess import batchProcess, getBatchInfo, updateBatchInfo
from ..userManagement.token import tokenCheck
from ..userManagement.userRank import getUserRankByUID


# 上传压缩包
def batchUpload_compress(request):
    user = str(request.POST.get("uid"))
    token = str(request.POST.get("token"))
    # 检查登录状态
    # print(tokenCheck(user, token), user, token)
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)

    if getUserRankByUID(user) != 2:
        # 不是超级用户，不能上传
        return HttpResponse(3)

    user = user.replace('.', '^')

    # 尝试解压缩
    packageFile = request.FILES.get("package")
    if packageFile is None:
        return HttpResponse(2)

    try:
        try:
            # 大的压缩包，django会保存在磁盘上
            srcFolderName = getCompressedFiles(str(packageFile), user, packageFile.temporary_file_path())
        except:
            # 小的压缩包，django会保存在内存里
            srcFolderName = getCompressedFile_inMemory(str(packageFile), user, packageFile)
    except Exception as e:
        return HttpResponse(2)

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


# 开始指定batch id的批处理
def startBatchProcess(request):
    user = str(request.POST.get("uid"))
    token = str(request.POST.get("token"))
    # 检查登录状态
    if not tokenCheck(user, token):
        # 1表示登录状态有问题
        return HttpResponse(1)
    batchID = ObjectId(request.POST.get("batchID"))
    batchInfo = getBatchInfo(batchID)

    # 只有状态4的批可以处理
    if batchInfo.get('status') != 4:
        # 状态不对，不能处理
        return HttpResponse(2)

    ignoreImage = request.POST.get("ignoreImage").split(',')
    imgList = batchInfo.get('imgList').split('|')
    totalNum = int(batchInfo.get('batchSize'))
    # print(ignoreImage)
    if ignoreImage[0] != '':
        # 预先去除不用处理的图片
        for ignore in ignoreImage:
            imgList.remove(ignore)
            deleteAllInfoOfImageBy_id(ObjectId(ignore))
            totalNum -= 1

    # 更新数据库，开始处理
    updateBatchInfo(batchID, {'status': 5, 'imgList': '|'.join(imgList), 'batchSize': totalNum})

    if totalNum != 0:
        processThread = threading.Thread(target=nbiImageProcessing, args=[batchID, user.replace('.', '^')])
        processThread.start()
        return HttpResponse(3)
    else:
        return HttpResponse(4)
