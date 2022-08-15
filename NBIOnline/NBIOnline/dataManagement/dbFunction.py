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


def deleteOneImage(type, name):
    typeOption = ['Green', 'Blue', 'NBI', 'Temp']
    if type not in typeOption:
        print("Can not find image type:{t}".format(t=type))
        return
    os.system("rm /home/ubuntu/NBI-Online/NBIOnline/static/Data/" + type + "/" + name)
