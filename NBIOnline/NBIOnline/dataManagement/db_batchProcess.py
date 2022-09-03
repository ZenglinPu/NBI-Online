import time
import pymongo

# '''
# 批处理批次信息表：BatchProcess
# | 字段名         | 类型    | 含义                 |
# | -------------- | ------- | ------------------------------------------------------------------------|
# | UID            | String  | 图片提交者的UID                                                           |
# | uploadTime     | Time    | 这一批次的上传时间                                                         |
# | expireTime     | Time    | 这一批次的过期时间                                                         |
# | imgList        | String  | 这一批次所有图片的_id，字符串形式，中间用|分割，其中每条数据是元组的形式             |
# | batchSize      | Integer | 这一批次的图片组数                                                         |
# | status         | Integer | 这一批次的处理状态，1-上传中；2-检查中；3-检查失败；4-检查成功；5-处理中；6-处理完成  |
# '''


# 批处理信息
class batchProcess:
    def __init__(self, uid):
        self.uid = uid
        self.imgList = []
        self.uploadTime = time.time()
        self.expireTime = time.time()
        self.batchSize = 0
        self.status = 1

    def addNewImageToBatch(self, greenImageName, blueImageName, whiteImageName, resultImageName, cImageName):
        self.imgList.append(str((greenImageName, blueImageName, whiteImageName, resultImageName, cImageName)))
        self.batchSize += 1

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['gidList'] = '|'.join(self.imgList)
        ret['uploadTime'] = self.uploadTime
        ret['expireTime'] = self.expireTime
        ret['batchSize'] = self.batchSize
        ret['status'] = 6   # 都在往后台存储了，那就是处理好了

    def saveData(self):
        print("Add New [Batch Process Data] at UID={u}".format(u=self.uid))
        conn = pymongo.MongoClient(
            'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
        table = conn.nbi.BatchProcess
        ret = table.insert_one(self.getDict())
        conn.close()
        return ret

