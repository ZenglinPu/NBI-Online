from doctest import FAIL_FAST
import time
import base64
import pymongo
import hmac
from datetime import datetime, timedelta


# 加密获得token的方法
# 过期时间设置为1个小时
from ..dataManagement.dbUtil import getConn, getTable, NBITABLE


def get_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 根据UID和token判断是否处于登录期间内
def TokenCheckLogin(uid, token):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.TokenInfo
    result = table.find({"UID": uid})
    conn.close()
    # 找不到该uid，未登录
    if result.count() == 0 or token is None:
        return 0, None

    # 找到uid
    for r in result:
        # 判断token是否相等
        recordToken = r.get("token")
        # print(recordToken,len(recordToken),token, len(token))
        if not recordToken == token + "=" * (len(recordToken) - len(token)):
            return 0, None
        # 判断是否过期
        expiresTime = r.get("expiresTime")
        # print(valid_date(expiresTime, datetime.now()))
        if not valid_date(expiresTime, datetime.now()):
            return 1, None

        # 每次check如果通过的话，就把过期的时间往后延1个小时
        from ..dataManagement.db_Token import UserToken
        newToken = UserToken(uid, datetime.now() + timedelta(hours=1))
        retToken = newToken.saveOrUpdateToken()
        return 2, retToken


# 比较时间
def valid_date(expireTime, nowTime):
    expireTime = time.mktime(expireTime.timetuple())
    nowTime = time.mktime(nowTime.timetuple())
    return expireTime > nowTime


# 检查提交的token有效性
def tokenCheck(uid, token):
    conn = getConn()
    table = getTable(conn, NBITABLE.TokenInfo)
    result = table.find({"UID": uid})
    conn.close()
    # 找不到，未登录
    if result.count() == 0 or token is None or uid is None:
        return False

    for r in result:
        # 判断token是否相等
        recordToken = r.get("token")
        # print(recordToken,len(recordToken),token, len(token))
        if not recordToken == token + "=" * (len(recordToken) - len(token)):
            return False
        # 判断是否过期
        expiresTime = r.get("expiresTime")
        if not valid_date(expiresTime, datetime.now()):
            return False
    return True


# 解码token的方法
# 返回布尔值判断是否匹配
# def out_token(key, token):
#     # token是前端传过来的token字符串
#     try:
#         token_str = base64.urlsafe_b64decode(token).decode('utf-8')
#         token_list = token_str.split(':')
#         if len(token_list) != 2:
#             return False
#         ts_str = token_list[0]
#         if float(ts_str) < time.time():
#             # token expired
#             return False
#         known_sha1_tsstr = token_list[1]
#         sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
#         calc_sha1_tsstr = sha1.hexdigest()
#         if calc_sha1_tsstr != known_sha1_tsstr:
#             # token certification failed
#             return False
#         # token certification success
#         return True
#     except Exception as e:
#         print(e)


# 根据token值返回用户id
# 0 - 没找到 ； -1 - 过期了
# def getUserByToken(token):
#     token = models.UserToken.objects.filter(token=token)
#     if token.count() == 0:
#         return 0
#     else:
#         token = token.first()
#         if datetime.now() > token.expiration_time:
#             return -1
#         else:
#             # 返回用户
#             return token.user_id

# 使得某个uid下的token过期
def logoutInToken(uid):
    conn = pymongo.MongoClient(
        'mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.TokenInfo
    newValue = {"$set": {"expiresTime": datetime.now()}}
    result = table.update_one({"UID": uid}, newValue)
    conn.close()
    return result
