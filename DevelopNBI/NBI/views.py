from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

"""返回HTML页面"""
def userLoginPage(request):
    return render(request, 'userPage_login.html')

def defaultToUserLoginPage(request):
    return HttpResponseRedirect("/NBI/User/login")

def mainPage(request):
    return render(request, 'mainPage.html')
    
def defaultToMainPage(request):
    return HttpResponseRedirect("/NBI/Image/mainPage")