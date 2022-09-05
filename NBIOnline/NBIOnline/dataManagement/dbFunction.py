import difflib
import math

from bson.objectid import ObjectId
import pymongo
import os


# 获取用户修改的上一张图片数据
def getLastImage(user):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    result = table.find({"UID": user}, sort=[('lastChangeTime', -1)])

    # 这个UID没有提交过数据
    if result.count() == 0:
        conn.close()
        return False

    # 这个UID提交过数据，查看是否是同样的图片
    conn.close()
    return result[0]


# 根据UID获取最近一次提交的数据的信息
def getInfoByUID(UID):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    ret = table.find_one({"UID": UID}, sort=[('lastChangeTime', -1)])
    conn.close()
    return ret


# 根据_id在图片数据表中提取数据
def getAllImageInfoBy_id(_id):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    table_addition = conn.nbi.PhotoAdditionInfo
    ret = table.find_one({'_id': ObjectId(_id)})
    ret_addition = table_addition.find_one({'gid': ObjectId(_id)})
    conn.close()
    return ret, ret_addition


# 根据_id在图片附加信息库中提取图片附加信息
def getAdditionalInfoBy_id(id):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoAdditionInfo
    ret = table.find_one({'gid': id})
    conn.close()
    return ret


# 根据打算注册的新UID检查是否已经注册
def checkUIDRegistered(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.UserInfo
    result = table.find({"UID": uid})
    if result.count() == 0:
        conn.close()
        return False
    conn.close()
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
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.PhotoInfo
    table_PhotoAdditionInfo = conn.nbi.PhotoAdditionInfo
    data = {}
    allInfo = table_PhotoInfo.find({'UID': user}).sort("lastChangeTime", -1)
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
    conn.close()
    return ret


# 根据user,filterType,filterValue获得数据
def getHistoryWithFilter(user, currentPage, pageCount, filterType, filterValue):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.PhotoInfo
    table_PhotoAdditionInfo = conn.nbi.PhotoAdditionInfo
    # 这个用户的所有数据
    allInfo = table_PhotoInfo.find({'UID': user}).sort("lastChangeTime", -1)
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
            if float(filterValue.split(',')[0]) <= info['uploadTime']*1000 <= float(filterValue.split(',')[1]):
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

    ret = {'info': data, 'totalPage': math.ceil(float((count-1) / pageCount)), 'totalImage': (count-1)}
    conn.close()
    return ret


# 根据_id删除一组图片的所有数据，包括图片本身，以及两个数据表中的数据
def deleteAllInfoOfImageBy_id(_id):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.PhotoInfo
    table_PhotoAdditionInfo = conn.nbi.PhotoAdditionInfo
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


# 字符串相似度
def similar_diff_ratio(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

# 存储更改的信息
def saveModification(id, sampleName, partName, preDiagnosis, pathologic, differentiation, cuttingEdge, remark):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoAdditionInfo = conn.nbi.PhotoAdditionInfo
    table_PhotoAdditionInfo.update_one({"gid": id},{"$set":{
        "sampleName":sampleName,
        "partName":partName,
        "preDiagnosis":preDiagnosis,
        "pathologic":pathologic,
        "differentiation":differentiation,
        "cuttingEdge":cuttingEdge,
        "remark":remark
        }})
    # 如果备注为空就不修改
    if remark is not None:
        table_PhotoAdditionInfo.update_one({"gid": id},{"$set":{"remark":remark}})
    conn.close()

# 获取批处理信息
def getBatchHistory(user, currentPage, pageCount):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_BatchProcess = conn.nbi.BatchProcess
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
            'uploadTime': str(object['uploadTime']),
            'expireTime': str(object['expireTime']),
            'status': str(object['status']),
        }
        data[count] = innerDict
        count += 1
        if count > end:
            break
    ret = {'info': data, 'totalPage': math.ceil(float(allInfo.count() / pageCount)), 'totalImage': allInfo.count()}
    conn.close()
    return ret