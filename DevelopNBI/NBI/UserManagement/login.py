import datetime
import json
from django.http import HttpResponse
import pymongo
from NBI.UserManagement.token import TokenCheckLogin
from NBI.UserManagement.md5 import transToMD5
from NBI.dataManagement.db_Token import UserToken
from NBI.dataManagement.db_User import getUnameByUID

# 检查登录
def loginCheck(request):
    uid = request.POST.get("uid")
    upw = request.POST.get("pwd")

    # 检查用户是否存在以及密码是否正确
    checkUserResult, uname = checkUserExist(uid)
    if not checkUserResult:
        # 1表示用户不存在，提示注册
        return HttpResponse(1)
    if not checkUserPW(uid, upw):
        # 2表示密码错误
        return HttpResponse(2)
    
    # 更新token并返回到前端
    newToken = UserToken(uid, datetime.datetime.now()+datetime.timedelta(hours=1))
    retNewToken = newToken.saveOrUpdateToken()

    ret = {
        'uid': uid,
        'token': retNewToken,
        'uname': uname,
    }
    ret = json.dumps(ret)
    return HttpResponse(ret,content_type='application/json')


def checkUserExist(uid):
    conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.UserInfo
    result = table.find({"UID":uid})
    if result.count() == 0:
        conn.close()
        return False, None
    for r in result:
        uname = r.get('name')
        break
    conn.close()
    return True, uname 


def checkUserPW(uid, pw):
    inputPW = transToMD5(pw)
    conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "49.232.229.126", "27017", "admin"))
    table = conn.nbi.UserInfo
    result = table.find_one({"UID":uid})
    if str(result.get("pwd")) != inputPW:
        return False
    return True

# 通过token和uid判断是否仍然处于登录状态内
def checkByToken(request):
    checkResult, newToken = TokenCheckLogin(request.POST.get("uid"), request.POST.get("token"))
    uname = getUnameByUID(request.POST.get("uid"))
    ret = {
        'check': checkResult,
        'token': newToken,
        'uname': uname,
    }
    ret = json.dumps(ret)
    return HttpResponse(ret,content_type='application/json')
