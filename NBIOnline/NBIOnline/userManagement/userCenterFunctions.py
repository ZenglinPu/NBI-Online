import json
import time

from django.http import HttpResponse

from ..userManagement.token import tokenCheck
from ..dataManagement.db_User import getUserInfoByUID, updateUname, updateAddInfo, inviteCodeReward, changePwd


# 修改用户名
def updateNewUName(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        updateUname(user, request.POST.get('name'))
        return HttpResponse(2)


def updateNewAddInfo(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        workPlace = request.POST.get("workPlace")
        department = request.POST.get("department")
        competent = request.POST.get("competent")
        updateAddInfo(user, workPlace, department, competent)
        ret = {
            "workPlace": workPlace,
            "department": department,
            "competent": competent,
        }
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')


# 用户中心，初始化查询数据
def getUserInfo(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        uInfo = getUserInfoByUID(user)
        # print(uInfo)
        ret = {
            "uid": uInfo.get("UID"),
            "name": uInfo.get("name"),
            "rank": getUserRank(uInfo.get("expiresTime")),
            "registerTime": getRegisterTime(uInfo.get("registerTime")),
            "workPlace": uInfo.get("workPlace"),
            "department": uInfo.get("department"),
            "competent": uInfo.get("competent"),
            "inviteCode": uInfo.get("inviteCode"),
            "SUM_generate": uInfo.get("SUM_generate"),
            "TIMES_generate": uInfo.get("TIMES_generate"),
            "expiresTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uInfo.get("expiresTime"))),
        }
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')


def getUserRank(et):
    if et >= int(time.time()):
        return 2
    return 1


def getRegisterTime(et):
    dt: str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(et))
    return dt


def checkInviteCode(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        inviteCode = request.POST.get("inviteCode").strip()
        result = inviteCodeReward(user, inviteCode)
        return HttpResponse(result)


def updateNewPwd(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        result = changePwd(user, request.POST.get("oldPwd"), request.POST.get("newPwd"))
        # 2表示原密码错误, 3表示成功
        if result:
            return HttpResponse(3)
        return HttpResponse(2)
