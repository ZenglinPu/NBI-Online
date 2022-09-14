import time
from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


# '''
# 批处理批次信息表：BatchProcess
# | 字段名         | 类型    | 含义                 |
# | -------------- | ------- | ------------------------------------------------------------------------|
# | UID            | String  | 图片提交者的UID                                                           |
# | batchName      | String  | 批次的名称                                                                |
# | srcFolderName  | String  | 存放原始图片数据的文件夹名称，其组成为{batchName}_{uid}{rand}                  |
# | uploadTime     | Time    | 这一批次的上传完成的时间                                                    |
# | checkTime      | Time    | 这一批次的解压缩、检查完成（通过或不通过）的时间                                 |
# | finishTime     | Time    | 这一批次的处理完成（处理错误）时间                                            |
# | expireTime     | Time    | 这一批次的过期时间                                                         |
# | imgList        | String  | 这一批次所有图片的_id，字符串形式，中间用'|'分割，其中每条数据是元组的形式           |
# | batchSize      | Integer | 这一批次的图片组数                                                         |
# | processedNum   | Integer | 这一批次已经处理的图片组数                                                   |
# | status         | Integer | 这一批次的处理状态，1-上传中；2-检查中；3-检查失败；4-检查成功；5-处理中；6-处理完成  |
# '''


# 批处理信息
class batchProcess:
    def __init__(self, uid, batchName):
        self.uid = uid
        self.batchName = batchName
        self.srcFolderName = None
        self.imgList = []
        self.uploadTime = time.time()
        self.expireTime = time.time() + 7*24*60*60  # 7天过期
        self.checkTime = None
        self.finishTime = None
        self.batchSize = 0
        self.processedNum = 0
        self.status = 2

    def addNewImageToBatch(self, greenImageName, blueImageName, whiteImageName, resultImageName, cImageName):
        self.imgList.append(str((greenImageName, blueImageName, whiteImageName, resultImageName, cImageName)))
        self.batchSize += 1

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['batchName'] = self.batchName
        ret['srcFolderName'] = self.srcFolderName
        ret['gidList'] = '|'.join(self.imgList)
        ret['uploadTime'] = self.uploadTime
        ret['checkTime'] = self.checkTime
        ret['finishTime'] = self.finishTime
        ret['expireTime'] = self.expireTime
        ret['batchSize'] = self.batchSize
        ret['processedNum'] = self.processedNum
        ret['status'] = self.status
        return ret

    def saveData(self):
        print("Add New [Batch Process Data] at UID={u}".format(u=self.uid))
        conn = getConnection()
        table = getTable(conn, NBITABLE.BatchProcess)
        ret = table.insert_one(self.getDict())
        # conn.close()
        return ret


# 提供一个字典和_id，更新batchProcess
def updateBatchInfo(_id, newValue):
    conn = getConnection()
    table = getTable(conn, NBITABLE.BatchProcess)
    condition = {'_id': _id}
    newValue = {"$set": newValue}
    result = table.update_one(condition, newValue)  # 执行数据库更新操作
    return result
