import pymongo
import time
import datetime
from ..ImageProcess.NBIGenerator import getRandom
import random


# '''
# 用户信息表: UserInfo
# | 字段名          | 类型   | 含义                                                                     |
# | -------------- | ------- | -------------------------------------------------------------------------|
# | UID            | String  | email地址                                                                |
# | pwd            | String  | md5加密后的密码                                                           |
# | validUser      | Integer | 用户注册后的状态：0-仅注册基本信息； 1-已经完善信息； 2-修改信息等待审核             |
# | registerTime   | Time    | 注册时间                                                                  |
# | name           | String  | 用户昵称（初始为随机）                                                     |
# | rank           | Integer | 用户等级：1-普通用户； 2-高级用户                                          |
# | expiresTime    | Time    | 高级用户过期时间戳                                                        |
# | workPlace      | String  | 用户工作单位（初始为空）                                                   |
# | department     | String  | 用户工作部门（初始为空）                                                   |
# | competent      | String  | 用户职称（初始为空）                                                       |
# | inviteCode     | String  | 邀请码                                                                    |
# '''

# '''
# 普通用户与高级用户的区别：
# 普通用户的下载图片是压缩后的图片，无法下载高清晰度原图；
# 普通用户每天有10次的生成次数限制;

# 普通用户与高级用户的判别：
# rank==2且当前时间没有超过它的高级用户过期时间戳
# '''

class User:
    def __init__(self, uid, pwd, registerTime=None, name=None, rank=2, expiresTime=None, workPlace=None,
                 department=None, competent=None):
        self.uid = uid
        self.pwd = pwd
        self.registerTime = time.time()
        if name is None:
            self.name = "User" + getRandom() + str(int(time.time()) % 10000)
        # 刚刚注册给予3天高级用户身份
        self.rank = rank
        self.expiresTime = time.mktime(
            time.strptime((datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d 00:00:00"),
                          '%Y-%m-%d %H:%M:%S'))
        self.workPlace = workPlace
        self.department = department
        self.competent = competent
        self.inviteCode = getInviteCode()

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['pwd'] = self.pwd
        ret['registerTime'] = self.registerTime
        ret['name'] = self.name
        ret['rank'] = self.rank
        ret['expiresTime'] = self.expiresTime
        ret['workPlace'] = self.workPlace
        ret['department'] = self.department
        ret['competent'] = self.competent
        ret['inviteCode'] = self.inviteCode
        return ret

    def saveNewUser(self):
        conn = pymongo.MongoClient(
            'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
        table = conn.nbi.UserInfo
        ret = table.insert_one(self.getDict())
        conn.close()
        return ret


def getInviteCode():
    #   digits="0123456789"
    ascii_letters = "abcdefghigklmnopqrstuvwxyz"
    str_list = [random.choice(ascii_letters) for i in range(30)]
    random_str = '~' + ''.join(str_list)
    return random_str


def getUnameByUID(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.UserInfo
    ret = table.find_one({'UID': uid})
    conn.close()
    if ret is not None:
        return ret.get("name")
    else:
        return "未登录"
