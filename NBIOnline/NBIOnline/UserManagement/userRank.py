# 用户等级权限管理相关操作
import time

import pymongo


def getUserRankByUID(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.UserInfo
    if table_PhotoInfo.find_one({"UID": uid})['expiresTime'] > time.time():
        conn.close()
        return 2
    conn.close()
    return 1


def checkUploadTime(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.UserInfo
    # print(table_PhotoInfo.find_one({"UID": uid})['TIMES_generate'])
    if table_PhotoInfo.find_one({"UID": uid})['TIMES_generate'] <= 0:
        conn.close()
        return False
    conn.close()
    return True
