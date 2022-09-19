import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..userManagement.token import tokenCheck
from ..dataManagement.dbFunction import getBatchImgData, getBatchDataWithFilter
# 进入historyData页面后，展示基本信息
def batchInfoDisplay(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # print(tokenCheck(user, token), token)
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        # 因为uid中存在特殊符号.
        # 在进行图片的处理中应当替换掉
        user = user.replace('.', '^')

        # 现在想要的是第几页
        currentPage = int(request.POST.get('currentPage'))
        # 每一页展示多少条数据
        pageCount = int(request.POST.get("pageCount"))
        bid = str(request.POST.get('bid'))
        ret = getBatchImgData(user, bid, currentPage, pageCount)
        # print(ret)
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')

def batchImgDataWithFilter(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)

        user = user.replace('.', '^')
        # bid批次id
        bid = request.POST.get('bid')
        # 现在想要的是第几页
        currentPage = int(request.POST.get('currentPage'))

        # 每一页展示多少条数据
        pageCount = int(request.POST.get("pageCount"))
        # 过滤的种类，目前是名称，部位和上传日期区间
        filterType = int(request.POST.get("filterType"))
        # 过滤的值，在前两个是字符串，后一个是两个时间戳
        filterValue = request.POST.get("filterValue")
        ret = getBatchDataWithFilter(user, bid, currentPage, pageCount, filterType, filterValue)
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')