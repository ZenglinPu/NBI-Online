from enum import Enum

import pymongo


# 用于管理mongodb的链接工具

class NBITABLE(Enum):
    # 为序列值指定value值
    PhotoInfo = 1
    UserInfo = 2
    TokenInfo = 3
    PhotoAdditionInfo = 4
    BatchProcess = 5


def getTable(conn, table):
    if table == NBITABLE.PhotoInfo:
        return conn.nbi.PhotoInfo
    elif table == NBITABLE.UserInfo:
        return conn.nbi.UserInfo
    elif table == NBITABLE.TokenInfo:
        return conn.nbi.TokenInfo
    elif table == NBITABLE.PhotoAdditionInfo:
        return conn.nbi.PhotoAdditionInfo
    elif table == NBITABLE.BatchProcess:
        return conn.nbi.BatchProcess
    else:
        print("No table:{t}".format(t=table))
        return None


global_connection = None


# DB连接的封装, 长连接
def getConnection():
    global global_connection
    while global_connection is None:
        try:
            if global_connection is not None:
                global_connection.close()
            global_connection = pymongo.MongoClient(
                'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
        except Exception as e:
            global_connection = None

    return global_connection
