import difflib
import math
import time

from bson.objectid import ObjectId
import os

from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


# 获取用户修改的上一张图片数据
def getLastImage(user):
    conn = getConnection()
    table = getTable(conn, NBITABLE.PhotoInfo)
    result = table.find({"UID": user}, sort=[('lastChangeTime', -1)])

    # 这个UID没有提交过数据
    if result.count() == 0:
        conn.close()
        return False

    # 这个UID提交过数据，查看是否是同样的图片
    # conn.close()
    return result[0]


# 根据UID获取最近一次提交的数据的信息
def getInfoByUID(UID):
    conn = getConnection()
    table = getTable(conn, NBITABLE.PhotoInfo)
    ret = table.find_one({"UID": UID}, sort=[('lastChangeTime', -1)])
    # conn.close()
    return ret


# 根据_id在图片数据表中提取数据
def getAllImageInfoBy_id(_id):
    conn = getConnection()
    table = getTable(conn, NBITABLE.PhotoInfo)
    table_addition = getTable(conn, NBITABLE.PhotoAdditionInfo)
    ret = table.find_one({'_id': ObjectId(_id)})
    ret_addition = table_addition.find_one({'gid': ObjectId(_id)})
    # conn.close()
    return ret, ret_addition


# 根据_id在图片附加信息库中提取图片附加信息
def getAdditionalInfoBy_id(id):
    conn = getConnection()
    table = getTable(conn, NBITABLE.PhotoAdditionInfo)
    ret = table.find_one({'gid': id})
    # conn.close()
    return ret


# 根据打算注册的新UID检查是否已经注册
def checkUIDRegistered(uid):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    result = table.find({"UID": uid})
    if result.count() == 0:
        conn.close()
        return False
    # conn.close()
    return True


def deleteOneImage(t, name):
    typeOption = ['Green', 'Blue', 'NBI', 'White', 'Temp']
    if t not in typeOption:
        print("Can not find image type:{t}".format(t=t))
        return
    if name is not None:
        os.system("rm /home/ubuntu/NBI-Online/NBIOnline/static/Data/" + t + "/" + name)


# 提取HistoryData页面所需的基础信息，无筛选条件，数据按照lastChangeTime逆序返回
def getHistory(user, currentPage, pageCount):
    conn = getConnection()
    table_PhotoInfo = getTable(conn, NBITABLE.PhotoInfo)
    table_PhotoAdditionInfo = getTable(conn, NBITABLE.PhotoAdditionInfo)
    data = {}
    allInfo = table_PhotoInfo.find({'UID': user, 'isBatch': False}).sort("lastChangeTime", -1)
    """
    我们当前每一页展示pageCount张图，
    目前需要的数据是currentPage页的数据，
    因此应该先跳过前(currentPage-1)*pageCount条的数据，
    然后取其之后的pageCount条数据
    """
    # 这里count就当作序号了，因此返回的数据其开头不一定是0，但是一定连续且不重复
    count = 1
    jump = (currentPage - 1) * pageCount  # 1 ~ jump的数据都不要
    end = currentPage * pageCount  # jump+1 ~ end的数据放进来，end+1的就不要了

    for object1 in allInfo:
        if count <= jump:
            count += 1
            continue
        _id = object1['_id']
        innerDict = {
            'index': count,
            '_id': str(_id),
            'Image_Compress': str(object1['Image_Compress']),
            'lastChangeTime': str(object1['lastChangeTime']),
            'expireTime': str(object1['expireTime']),
        }
        object2 = table_PhotoAdditionInfo.find_one({"gid": _id})
        innerDict['sampleName'] = object2['sampleName']
        innerDict['part'] = object2['part']
        innerDict['preDiagnosis'] = object2['preDiagnosis']
        data[count] = innerDict
        count += 1
        if count > end:
            break
    ret = {'info': data, 'totalPage': math.ceil(float(allInfo.count() / pageCount)), 'totalImage': allInfo.count()}
    # conn.close()
    return ret


# 根据user,filterType,filterValue获得数据
def getHistoryWithFilter(user, currentPage, pageCount, filterType, filterValue):
    conn = getConnection()
    table_PhotoInfo = getTable(conn, NBITABLE.PhotoInfo)
    table_PhotoAdditionInfo = getTable(conn, NBITABLE.PhotoAdditionInfo)
    # 这个用户的所有数据
    allInfo = table_PhotoInfo.find({'UID': user, 'isBatch': False}).sort("lastChangeTime", -1)
    data = {}
    count = 1
    jump = (currentPage - 1) * pageCount  # 1 ~ jump的数据都不要
    end = currentPage * pageCount  # jump+1 ~ end的数据放进来，end+1的就不要了
    # 根据筛选条件获得满足条件的数据
    if filterType == 1:
        # 名称模糊搜索
        for info in allInfo:
            additionInfo = table_PhotoAdditionInfo.find_one({"gid": info['_id']})
            # print(similar_diff_ratio(filterValue, additionInfo['sampleName']))
            if similar_diff_ratio(filterValue, additionInfo['sampleName']) > 0.76:
                if count <= jump:
                    count += 1
                    continue
                if count > end:
                    # 就不往返回的数据里加东西了，但是要继续计数
                    count += 1
                    continue
                _id = info['_id']
                innerDict = {'index': count, '_id': str(_id), 'Image_Compress': str(info['Image_Compress']),
                             'lastChangeTime': str(info['lastChangeTime']), 'expireTime': str(info['expireTime']),
                             'sampleName': additionInfo['sampleName'], 'part': additionInfo['part'],
                             'preDiagnosis': additionInfo['preDiagnosis']}
                data[count] = innerDict
                count += 1

    elif filterType == 2:
        # 部位搜索
        for info in allInfo:
            additionInfo = table_PhotoAdditionInfo.find_one({"gid": info['_id']})
            # print(similar_diff_ratio(filterValue, additionInfo['part']))
            if similar_diff_ratio(filterValue, additionInfo['part']) > 0.9:
                if count <= jump:
                    count += 1
                    continue
                if count > end:
                    count += 1
                    continue
                _id = info['_id']
                innerDict = {'index': count, '_id': str(_id), 'Image_Compress': str(info['Image_Compress']),
                             'lastChangeTime': str(info['lastChangeTime']), 'expireTime': str(info['expireTime']),
                             'sampleName': additionInfo['sampleName'], 'part': additionInfo['part'],
                             'preDiagnosis': additionInfo['preDiagnosis']}
                data[count] = innerDict
                count += 1

    elif filterType == 3:
        # 时间范围内搜索
        for info in allInfo:
            additionInfo = table_PhotoAdditionInfo.find_one({"gid": info['_id']})
            # print(float(filterValue.split(',')[0]) , info['uploadTime'], float(filterValue.split(',')[1]))
            if float(filterValue.split(',')[0]) <= info['uploadTime'] * 1000 <= float(filterValue.split(',')[1]):
                if count <= jump:
                    count += 1
                    continue
                if count > end:
                    count += 1
                    continue
                _id = info['_id']
                innerDict = {'index': count, '_id': str(_id), 'Image_Compress': str(info['Image_Compress']),
                             'lastChangeTime': str(info['lastChangeTime']), 'expireTime': str(info['expireTime']),
                             'sampleName': additionInfo['sampleName'], 'part': additionInfo['part'],
                             'preDiagnosis': additionInfo['preDiagnosis']}
                data[count] = innerDict
                count += 1

    ret = {'info': data, 'totalPage': math.ceil(float((count - 1) / pageCount)), 'totalImage': (count - 1)}
    # conn.close()
    return ret


# 根据_id删除一组图片的所有数据，包括图片本身，以及两个数据表中的数据
def deleteAllInfoOfImageBy_id(_id):
    conn = getConnection()
    table_PhotoInfo = getTable(conn, NBITABLE.PhotoInfo)
    table_PhotoAdditionInfo = getTable(conn, NBITABLE.PhotoAdditionInfo)
    info_image = table_PhotoInfo.find_one({"_id": ObjectId(_id)})
    # print(info_image)
    # print(info_imageAddition)
    try:
        # 删除图片
        deleteOneImage("NBI", info_image.get("Image_Result"))
        deleteOneImage("Green", info_image.get("Image_Green"))
        deleteOneImage("Blue", info_image.get("Image_Blue"))
        deleteOneImage("White", info_image.get("Image_White"))
        deleteOneImage("Temp", info_image.get("Image_Compress"))
        # 清空数据库
        table_PhotoInfo.delete_one({"_id": ObjectId(_id)})
        table_PhotoAdditionInfo.delete_one({"gid": ObjectId(_id)})
        return True
    except Exception as e:
        return False


# 删除所有过期图片
# TODO: 目前仅删除图片本身以及其在两个图片数据表中数据，未对batch_process表数据进行处理
def deleteAllExpiredImages():
    conn = getConnection()
    table = getTable(conn, NBITABLE.PhotoInfo)
    current_time = time.time()

    # 根据时间戳判断是否过期
    for expired_image in table.find({"expireTime": {"$lt": current_time}}):
        deleteAllInfoOfImageBy_id(expired_image["_id"])
    # conn.close()


# 字符串相似度
def similar_diff_ratio(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


# 存储更改的信息
def saveModification(id, sampleName, partName, preDiagnosis, pathologic, differentiation, infiltration, cuttingEdge, remark):
    conn = getConnection()
    table_PhotoAdditionInfo = getTable(conn, NBITABLE.PhotoAdditionInfo)
    print(table_PhotoAdditionInfo)
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"sampleName": sampleName}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"part": partName}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"preDiagnosis": preDiagnosis}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"pathologic": pathologic}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"differentiation": differentiation}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"infiltration": infiltration}})
    table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"cuttingEdge": cuttingEdge}})

    # table_PhotoAdditionInfo.update_one({"gid": id}, {"$set": {
    #     "sampleName": sampleName,
    #     "partName": partName,
    #     "preDiagnosis": preDiagnosis,
    #     "pathologic": pathologic,
    #     "differentiation": differentiation,
    #     "infiltration": infiltration,
    #     "cuttingEdge": cuttingEdge,
    # }})
    # 如果备注为空就不修改
    if remark is not None:
        table_PhotoAdditionInfo.update_one({"gid": ObjectId(id)}, {"$set": {"remark": remark}})
    # conn.close()


# 获取批处理信息
def getBatchHistory(user, currentPage, pageCount):
    conn = getConnection()
    table_BatchProcess = getTable(conn, NBITABLE.BatchProcess)
    data = {}
    allInfo = table_BatchProcess.find({'UID': user}).sort("lastChangeTime", -1)
    """
    我们当前每一页展示pageCount张图，
    目前需要的数据是currentPage页的数据，
    因此应该先跳过前(currentPage-1)*pageCount条的数据，
    然后取其之后的pageCount条数据
    """
    # 这里count就当作序号了，因此返回的数据其开头不一定是0，但是一定连续且不重复
    count = 1
    jump = (currentPage - 1) * pageCount  # 1 ~ jump的数据都不要
    end = currentPage * pageCount  # jump+1 ~ end的数据放进来，end+1的就不要了

    for object in allInfo:
        if count <= jump:
            count += 1
            continue
        _id = object['_id']
        innerDict = {
            'index': count,
            '_id': str(_id),
            'Image_Result': str(object['Image_Result']),
        }
        data[count] = innerDict
        count += 1
        if count > end:
            break
    ret = {'info': data, 'totalPage': math.ceil(float(allInfo.count() / pageCount)), 'totalImage': allInfo.count()}
    # conn.close()
    return ret


# 根据_id查询一个批次的状态信息，包括当前的处理状态，以及一些时间戳
def getBatchStatusByID(_id):
    conn = getConnection()
    table_batch = getTable(conn, NBITABLE.BatchProcess)
    info = table_batch.find_one({'_id': _id})
    ret = {
        'status': info.get('status'),
        'uploadTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.get('uploadTime'))),
        'checkTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.get('checkTime'))),
        'finishTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.get('finishTime'))),
        'batchSize': info.get('batchSize'),
        'processedNum': info.get('processedNum'),
    }
    return ret


# 根据_id查询一个批次所有原始图片，由于很多原始图片很大，这一步可能会很慢
# 注意，这一步需要在检查完成之后进行，在这一步完成之后才能确保图片都成组，并且已经生成了压缩图片
def getOriginImage(_id):
    pass