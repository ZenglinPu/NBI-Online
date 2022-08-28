# 用户等级权限管理相关操作
import time

import pymongo


def getUserRankByUID(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table_PhotoInfo = conn.nbi.UserInfo
    if table_PhotoInfo.find_one({"UID": uid})['expiresTime'] > time.time():
        return 2
    return 1
