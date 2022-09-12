from datetime import datetime
from ..userManagement.token import get_token  # 获取新随机token
import pymongo
from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


# '''
# 用户token表：TokenInfo
# | 字段名         | 类型    | 含义                 |
# | -------------- | ------- | --------------------|
# | UID            | String  | email地址           |
# | expiresTime    | Time    | token过期时间        |
# | token          | String  | token值             |
# | lastLoginTime  | Time    | 上一次登录的时间     |
# '''

class UserToken:
    def __init__(self, uid, expiresTime, token=None, lastLoginTime=None):
        self.uid = uid
        self.expiresTime = expiresTime
        self.token = token
        # 无论是首次登录创建token还是后续登录创建token，这个都是now
        if lastLoginTime is None:
            self.lastLoginTime = datetime.now()

    def getRandomToken(self):
        return get_token(self.uid)

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['expiresTime'] = self.expiresTime
        if self.token is None:
            self.token = self.getRandomToken()
        ret['token'] = self.token
        ret['lastLoginTime'] = self.lastLoginTime
        return ret

    # 检查token是否存在，不存在则创建，存在则更新
    def saveOrUpdateToken(self):
        conn = getConnection()
        table = getTable(conn, NBITABLE.TokenInfo)
        tryFind = table.find({"UID": self.uid})
        tokenDict = self.getDict()
        if tryFind.count() == 0:
            # 新增并添加到数据库
            table.insert_one(tokenDict)
        else:
            # 更新过期时间和token值
            condition = {"UID": self.uid}
            table.replace_one(condition, tokenDict)
            pass
        conn.close()
        return tokenDict.get("token")
