
# '''
# 用户信息表: ValidateCode
# | 字段名          | 类型   | 含义                                                                     |
# | -------------- | ------- | -------------------------------------------------------------------------|
# | UID            | String  | email地址                                                                |                                                       |
# | expairsTime    | Time    | 过期时间                                                                  |
# | code           | String  | 验证码                                                     |
# '''

import datetime
import time
from ..dataManagement.db_connection import getConnection, getTable, NBITABLE


class ValidateCode:
    def __init__(self, uid, code):
        self.uid = uid
        self.code = code
        # 验证码创建5分钟后过期
        self.expiresTime = time.time() + 60 * 5

    def getDict(self):
        ret = dict()
        ret['UID'] = self.uid
        ret['code'] = self.code
        ret['expiresTime'] = self.expiresTime
        return ret

    def saveNewValidateCode(self):
        print("Add New [Valideta Code] at UID={u}".format(u=self.uid))
        conn = getConnection()
        table = getTable(conn, NBITABLE.ValidateCode)
        ret = table.insert_one(self.getDict())
        return ret

# 检查邮箱地址所对应验证码
def checkValidateCode(email, vcode):
    conn = getConnection()
    table = getTable(conn, NBITABLE.ValidateCode)
    # 找到email对应的最新验证码
    ret = table.find_one({'UID': email}, sort=[('expiresTime', -1)])
    if ret is None:
        # 没有找到对应验证码
        return -1
    # 找到验证码了，判断是否过期
    if ret['expiresTime'] < time.time():
        # 过期了
        return -2
    if ret['code'] != vcode:
        return -3
    return 0