import json
from django.http import HttpResponse
from ..userManagement.token import tokenCheck
from ..dataManagement.dbFunction import getHistory


# 进入historyData页面后，展示基本信息
def historyDisplay(request):
    if request.method == 'POST':
        user = request.POST.get('uid')
        token = request.POST.get('token')
        # 检查登录状态
        if not tokenCheck(user, token):
            # 1表示登录状态有问题
            return HttpResponse(1)
        # 因为uid中存在特殊符号.
        # 在进行图片的处理中应当替换掉
        user = user.replace('.', '*')

        ret = getHistory()
        ret = json.dumps(ret)
        return HttpResponse(ret, content_type='application/json')
