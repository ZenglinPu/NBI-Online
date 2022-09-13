import pymongo
import time
import datetime
from ..imageProcess.NBIGenerator import getRandom
import random
from ..dataManagement.db_connection import getConnection, getTable, NBITABLE

# '''
# 用户信息表: UserInfo
# | 字段名          | 类型   | 含义                                                                     |
# | -------------- | ------- | -------------------------------------------------------------------------|
# | UID            | String  | email地址                                                                |
# | pwd            | String  | md5加密后的密码                                                           |
# | registerTime   | Time    | 注册时间                                                                  |
# | name           | String  | 用户昵称（初始为随机）                                                     |
# | expiresTime    | Time    | 高级用户过期时间戳                                                        |
# | workPlace      | String  | 用户工作单位（初始为空）                                                   |
# | department     | String  | 用户工作部门（初始为空）                                                   |
# | competent      | String  | 用户职称（初始为空）                                                       |
# | inviteCode     | String  | 邀请码                                                                  |
# | isSend         | Boolean | 是否已经赠送过邀请码？true表示已经赠送（每人赠送一次，可多次接受）                  |
# | SUM_generate   | Integer | 记录用户生成的总NBI张数                                                    |
# | TIMES_generate | Integer | 可生成NBI图片数，超级用户为不限，也为10，但是上传时不会减少，普通用户为10            |
# '''

# '''
# 普通用户与高级用户的区别：
# 普通用户的下载图片是压缩后的图片，无法下载高清晰度原图；
# 普通用户有10次的生成次数限制;
# 如果上传图片不生成，则保留24小时，如果生成了，普通用户30天，高级用户1年

# 普通用户与高级用户的判别：
# 当前时间没有超过它的高级用户过期时间戳
# '''
from ..userManagement.md5 import transToMD5


class User:
    def __init__(self, uid, pwd, name=None, workPlace=None,
                 department=None, competent=None):
        self.uid = uid
        self.pwd = pwd
        self.registerTime = time.time()
        if name is None:
            self.name = "User" + getRandom() + str(int(time.time()) % 10000)
        # 刚刚注册给予3天高级用户身份
        self.expiresTime = time.mktime(
            time.strptime((datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d 00:00:00"),
                          '%Y-%m-%d %H:%M:%S'))
        self.workPlace = workPlace
        self.department = department
        self.competent = competent
        self.inviteCode = getInviteCode()
        self.isSend = False
        self.SUM_generate = 0
        self.TIMES_generate = 10

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['pwd'] = self.pwd
        ret['registerTime'] = self.registerTime
        ret['name'] = self.name
        ret['expiresTime'] = self.expiresTime
        ret['workPlace'] = self.workPlace
        ret['department'] = self.department
        ret['competent'] = self.competent
        ret['inviteCode'] = self.inviteCode
        ret['isSend'] = self.isSend
        ret['SUM_generate'] = self.SUM_generate
        ret['TIMES_generate'] = self.TIMES_generate
        return ret

    def saveNewUser(self):
        print("Add New [User Data] at UID={u}".format(u=self.uid))
        conn = getConnection()
        table = getTable(conn, NBITABLE.UserInfo)
        ret = table.insert_one(self.getDict())
        conn.close()
        return ret


def getInviteCode():
    #   digits="0123456789"
    ascii_letters = "0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    str_list = [random.choice(ascii_letters) for i in range(35)]
    random_str = '~' + ''.join(str_list)
    return random_str


def getUnameByUID(uid):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    ret = table.find_one({'UID': uid})
    conn.close()
    if ret is not None:
        return ret.get("name")
    return "未登录"


def getUserInfoByUID(uid):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    ret = table.find_one({'UID': uid})
    conn.close()
    if ret is not None:
        return ret
    return None


def updateUname(uid, uname):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    newValue = {"$set": {"name": uname}}
    result = table.update_one({"UID": uid}, newValue)
    conn.close()
    return result


def updateAddInfo(uid, workPlace, department, competent):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    newValue = {"$set": {"workPlace": workPlace, "department": department, "competent": competent}}
    result = table.update_one({"UID": uid}, newValue)
    conn.close()
    return result


# 生成总条数加一，同时会更新剩余生成次数，但是要根据用户等级
def addSumGenerate(uid):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    oldTimes = table.find_one({"UID": uid})['SUM_generate']
    newValue = {"$set": {"SUM_generate": oldTimes + 1}}
    if table.find_one({"UID": uid})['expiresTime'] < time.time():
        # 不是超级用户了，那么需要将次数-1
        oldSum = int(table.find_one({"UID": uid})['TIMES_generate'])
        table.update_one({"UID": uid}, {"$set": {"TIMES_generate": oldSum - 1}})
    table.update_one({"UID": uid}, newValue)
    conn.close()


# 根据邀请码查询用户信息，满足要求则给予奖励并返回true,失败返回false
def inviteCodeReward(uid, inviteCode):
    # 检查用户是否为刚注册第一天内
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    isSend = table.find_one({"UID": uid})['isSend']
    if isSend:
        return -4  # 表示已经送过了
    registerTime = table.find_one({"UID": uid})['registerTime']
    oneDayLater = registerTime + 24 * 60 * 60
    if time.time() >= oneDayLater:
        return -1  # 表示过时了
    targetUID = table.find({"inviteCode": inviteCode})
    if targetUID.count() != 1:
        return -2  # 表示找不到那个人，可能输错了
    targetUser = targetUID[0]
    # 排除自己邀请自己的情况
    if targetUser['UID'] == uid:
        return -3

    newValue = {"$set": {"isSend": True}}
    table.update_one({"UID": uid}, newValue)

    addSuperDay(targetUser, 30)
    conn.close()
    return 1


def addSuperDay(user, num):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    # 先看是否是超级用户，如果是就直接加上时间，不是则在当前的基础上加上时间
    if user['expiresTime'] >= time.time():
        # 没过期
        newExpiresTime = user['expiresTime'] + num * 24 * 60 * 60
    else:
        newExpiresTime = time.time() + num * 24 * 60 * 60
    newValue = {"$set": {"expiresTime": newExpiresTime, "TIMES_generate": 10}}
    table.update_one({"UID": user["UID"]}, newValue)
    conn.close()


# 输入旧密码，更新为新密码，旧密码不对则返回false,对的则返回true,并且更新
def changePwd(uid, oldPwd, newPwd):
    conn = getConnection()
    table = getTable(conn, NBITABLE.UserInfo)
    oldPwdInDatabase = table.find_one({"UID": uid})['pwd']
    if not transToMD5(oldPwd) == oldPwdInDatabase:
        return False
    newValue = {"$set": {"pwd": transToMD5(newPwd)}}
    table.update_one({"UID": uid}, newValue)
    conn.close()
    return True
