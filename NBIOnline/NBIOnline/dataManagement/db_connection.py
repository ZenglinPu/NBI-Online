from enum import Enum

import pymongo
from ..configLoader import nbi_conf


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
    conf = nbi_conf.configs
    while global_connection is None:
        try:
            if global_connection is not None:
                global_connection.close()
            global_connection = pymongo.MongoClient(
                'mongodb://{}:{}@{}:{}/?authSource={}'.format(conf['db_user'], conf['db_password'], conf['db_address'], conf['db_port'],
                                                              conf['db_authsource']))
        except Exception as e:
            print('Try to reconnect database.')
            global_connection = None

    return global_connection
