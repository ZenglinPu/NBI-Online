import math
from bson.objectid import ObjectId
import pymongo
import os


# 获取用户修改的上一张图片数据
def getLastImage(user):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    result = table.find({"UID": user})

    # 这个UID没有提交过数据
    if result.count() == 0:
        conn.close()
        return False

    # 这个UID提交过数据，查看是否是同样的图片
    ret = getInfobyUID(user)
    conn.close()
    return ret


# 根据UID获取最近一次提交的数据的信息
def getInfobyUID(UID):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    ret = table.find_one(sort=[('lastChangeTime', -1)])
    conn.close()
    return ret


# 根据_id在图片数据表中提取数据
def getAllImageInfoBy_id(_id):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    table_addition = conn.nbi.PhotoAdditionInfo
    ret = table.find_one({'_id':ObjectId(_id)})
    ret_addition = table_addition.find_one({'gid':ObjectId(_id)})
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
    ret = {}
    data = {}
    allInfo = table_PhotoInfo.find({'UID': user}).sort("lastChangeTime", -1)
    ret['totalPage'] = math.ceil(float(allInfo.count() / pageCount))
    ret['totalImage'] = allInfo.count()
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
    ret['info'] = data
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