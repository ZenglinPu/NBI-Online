import os
import time

import pymongo
from ..dataManagement.db_connection import getConnection


# 管理数据库的函数，谨慎调用

# system manager
class NBIManager():
    def __init__(self, table):
        self.__conn = getConnection()
        if table == "PhotoInfo":
            self.__table = self.__conn.nbi.PhotoInfo
        elif table == "UserInfo":
            self.__table = self.__conn.nbi.UserInfo
        elif table == "TokenInfo":
            self.__table = self.__conn.nbi.TokenInfo
        elif table == "PhotoAdditionInfo":
            self.__table = self.__conn.nbi.PhotoAdditionInfo
        elif table == "BatchProcess":
            self.__table = self.__conn.nbi.BatchProcess
        else:
            print("No table:{t}".format(t=table))

    def closeConnection(self):
        self.__conn.close()

    def getTable(self):
        return self.__table

    def printAll(self):
        result = self.__table.find()
        for r in result:
            print(r)

    def removeData(self, condition):
        self.__table.remove(condition)

    # 清除数据表中的所有图片数据
    def removeAllTableData(self):
        if input("Make sure you want to clear all data in table {t}[y/N]:".format(t=self.__table)) == 'y':
            self.__table.remove()

    # 清除所有磁盘中的图片数据
    # only work on linux
    def clearAllImageData(self):
        if input("Make sure you want to clear all image data[y/N]:") == 'y':
            os.system("rm -rf /home/ubuntu/NBI-Online/NBIOnline/static/Data")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data/Blue")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data/White")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data/Green")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data/NBI")
            os.system("mkdir /home/ubuntu/NBI-Online/NBIOnline/static/Data/Temp")


# manager = NBIManager("UserInfo")
# manager.clearAllImageData()
# manager.removeAllTableData()
# manager.printAll()
print(time.time())
