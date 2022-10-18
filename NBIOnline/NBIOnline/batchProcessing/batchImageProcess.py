import os
import time
import shutil

from bson import ObjectId

from ..dataManagement.db_ImageAdditionInfo import imageAdditionInfo
from ..dataManagement.db_ImageData import imageData
from ..dataManagement.db_batchProcess import updateBatchInfo, getBatchInfo
from ..imageProcess.ImageProcesser import transPackageImage, processImageByID


# 处理已经检查好的图片数据，更新单张图片的数据库
def nbiImageProcessing(*args):
    batchID = args[0]
    uid = args[1]

    batchInfo = getBatchInfo(batchID)
    processNum = batchInfo.get("processedNum")
    for img_id in batchInfo.get('imgList').split('|'):
        try:
            processImageByID(uid, ObjectId(img_id))
        except Exception as e:
            updateBatchInfo(batchID, {'status': 7})
            raise e
        processNum += 1
        updateBatchInfo(batchID, {'processedNum': processNum})
    # 成功处理完成
    updateDict = {
        'status': 6,
        'finishTime': time.time(),
        'processedNum': processNum,
    }
    updateBatchInfo(batchID, updateDict)


# 图片预处理，检查，成组，更新数据库，放到对应的路径下
def batchImagePreProcessing(*args):
    batchID = args[0]
    originPath = "../NBIOnline/static/Data/Batch/" + args[1]

    # 用来记录更新数据库
    totalPare = 0
    imgList = []

    try:
        while len(os.listdir(originPath)) > 0:
            # 选取第一张图片
            img_pareName, img_pareType, img_type = getNameAndType(os.listdir(originPath)[0])
            isFindBlue = False
            isFindGreen = False

            if img_pareType == "B" or img_pareName == "b":
                isFindBlue = True
            if img_pareType == "G" or img_pareName == "g":
                isFindGreen = True

            # 用来记录已经配对的图片名称
            toMoveList = [os.listdir(originPath)[0]]
            # print(img_pareName, img_pareType, img_type)
            # 遍历整个文件夹，寻找配对
            for i in os.listdir(originPath):
                pn, pt, rt = getNameAndType(i)
                # print(pn, pt, rt)
                if pn == img_pareName:
                    if pt == img_pareType:
                        continue
                    # 找到配对
                    else:
                        if pt == "B" or pt == "b":
                            isFindBlue = True
                        if pt == "G" or pt == "g":
                            isFindGreen = True
                        toMoveList.append(getFullName(pn, pt, rt))

            # 仅有在既有蓝色又有绿色的时候才移动图片，否则依然检查不通过，白色无所谓
            if isFindGreen and isFindBlue:
                totalPare += 1
                imgList.append(str(transToStorage(originPath, toMoveList, args[2])))
                for moveAbleImage in toMoveList:
                    os.remove(originPath+'/'+moveAbleImage)
            else:
                # 检查没有通过，通过_id更新数据库
                updateBatchInfo(batchID, {'batchSize': totalPare, 'checkTime': time.time(), 'status': 3, 'imgList': '|'.join(imgList)})
                os.remove(originPath)
                return

        # 检查通过，通过_id更新数据库
        updateBatchInfo(batchID, {'batchSize': totalPare, 'checkTime': time.time(), 'status': 4, 'imgList': '|'.join(imgList)})
        shutil.rmtree(originPath)
        return
    except Exception as e:
        updateBatchInfo(batchID,
                        {'batchSize': totalPare, 'checkTime': time.time(), 'status': 3, 'imgList': '|'.join(imgList)})
        os.remove(originPath)
        raise e


def getNameAndType(fullName):
    first = str(fullName).split('.')[0].split('_')
    return first[0], first[1], str(fullName).split('.')[1]


def getFullName(img_pareName, img_pareType, img_type):
    return img_pareName + '_' + img_pareType + '.' + img_type


# 将一组图片从Batch路径下处理到对应的路径下，同时，如果有raw格式的图片则转变后再存过去
# 移动后会在数据库中创建新数据，并返回新数据的_id
# 不会删除原图片
def transToStorage(originPath, toMoveList, uid):
    imageBlue = imageGreen = imageWhite = None
    sampleName = getNameAndType(toMoveList[0])[0]
    for i in toMoveList:
        if getNameAndType(i)[1] == "B" or getNameAndType(i)[1] == 'b':
            imageBlue = originPath + '/' + i
            continue
        if getNameAndType(i)[1] == "G" or getNameAndType(i)[1] == 'g':
            imageGreen = originPath + '/' + i
            continue
        if getNameAndType(i)[1] == "W" or getNameAndType(i)[1] == 'w':
            imageWhite = originPath + '/' + i
            continue
    image_blue_name, image_green_name, image_white_name = transPackageImage(imageBlue, imageGreen, imageWhite)
    newImageData = imageData(
        uid=uid,
        image_green=image_green_name,
        image_blue=image_blue_name,
        image_white=image_white_name,
        image_result=None,
        image_compress=None,
        lastChangeTime=time.time(),
        isBatch=True,
    )
    gid = newImageData.saveData().inserted_id
    newAdditionInfo = imageAdditionInfo(
        gid=gid,
        sampleName=sampleName,
        part=None,
        remark=None,
        preDiagnosis=None,
    )
    newAdditionInfo.saveNewAdditionalInfo()
    return gid

