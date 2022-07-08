import pymongo
import os

def getLastImage(user):
    conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
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
    conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    ret = table.find_one(sort=[('LastChangeTime', -1)])
    conn.close()
    return ret
    
# 根据打算注册的新UID检查是否已经注册
def checkUIDRegistered(uid):
    conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.UserInfo
    result = table.find({"UID":uid})
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
    os.system("rm /home/ubuntu/DevelopNBI/static/Data/"+type+"/"+name)
    