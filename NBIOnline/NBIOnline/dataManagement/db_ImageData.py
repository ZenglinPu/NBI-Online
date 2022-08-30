import time
import pymongo


# '''
# 图片生成信息表：PhotoInfo
# | 字段名         | 类型    | 含义                 |
# | -------------- | ------- | -------------------------------------------------------------------------|
# | UID            | String  | 图片提交者的UID                                                           |
# | Image_Green    | String  | 绿光图片名                                                                |
# | Image_White    | String  | 白光图片名(可以为空)                                                       |
# | Image_Blue     | String  | 蓝光图片名                                                                |
# | Image_Result   | String  | NBI合成图片名                                                             |
# | Image_Compress | String  | NBI合成后的压缩图片名(这个供前端展示)                                         |
# | uploadTime     | Time    | 源图片上传时间                                                            |
# | lastChangeTime | Time    | 上一次的修改时间                                                           |
# | expireTime     | Time    | 图片数据自动删除的时间，None则表示永久保存                                  |
# | isAutoBrightness| Boolean| 最后一次生成时是否自动调节亮度                                              |
# | isGenerated    | Boolean | 是否点击了生成按钮，没有的则默认保留24小时                                    |
# | contrast       | Integer | 最后一次生成时的对比度                                                     |
# | light          | Integer | 最后一次生成时的亮度                                                       |
# | saturation     | Integer | 最后一次生成时的饱和度                                                     |
# | channelOffset  | Integer | 最后一次生成时的通道调整值                                                 |
# '''

# image data
class imageData:
    def __init__(self, uid, image_green=None, isAutoBrightness=None, image_blue=None, image_white=None,
                 image_result=None, image_compress=None, lastChangeTime=None):
        self.uid = uid
        self.image_blue = image_blue
        self.image_green = image_green
        self.image_white = image_white
        self.image_result = image_result
        self.image_compress = image_compress
        self.uploadTime = time.time()
        self.lastChangeTime = lastChangeTime
        self.expireTime = self.uploadTime + 24 * 60 * 60  # 在刚刚上传时生成这条数据，过期时间默认设置为24小时后
        self.isAutoBrightness = isAutoBrightness
        self.isGenerated = False
        self.contrast = None
        self.light = None
        self.saturation = None
        self.channelOffset = None

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['Image_Green'] = self.image_green
        ret['Image_Blue'] = self.image_blue
        ret['Image_White'] = self.image_white
        ret['Image_Result'] = self.image_result
        ret['Image_Compress'] = self.image_compress
        ret['lastChangeTime'] = self.lastChangeTime
        ret['uploadTime'] = self.uploadTime
        ret['expireTime'] = self.expireTime
        ret['contrast'] = None
        ret['light'] = None
        ret['saturation'] = None
        ret['channelOffset'] = None
        ret['isAutoBrightness'] = self.isAutoBrightness
        ret['isGenerated'] = self.isGenerated
        return ret

    # 创建新数据并保存
    def saveData(self):
        print("Add New Data at UID={u}".format(u=self.uid))
        conn = pymongo.MongoClient(
            'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
        table = conn.nbi.PhotoInfo
        ret = table.insert_one(self.getDict())
        conn.close()
        return ret


# 替换原有数据，依据_id，不能依据UID，这样会更新掉所有这个Uid下的数据，造成错误
def updateImageData(_id, updateValue):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.PhotoInfo
    condition = {'_id': _id}
    newValue = {"$set": updateValue}
    result = table.update_one(condition, newValue)  # 执行数据库更新操作
    conn.close()
    return result
