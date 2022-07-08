from django.urls import path
from django.contrib import admin
from .UserManagement.register import sendValidCodeEmail, registerNewUser
from .UserManagement.login import loginCheck, checkByToken
from .ImageProcess.requestFunctions import updateInputAndGetNBI, uploadImage, chooseLastImage
from .views import defaultToUserLoginPage, defaultToMainPage, mainPage, userLoginPage

urlpatterns = [
    path(r'NBI/admin/', admin.site.urls),

    # '''Image Process'''
    path(r'NBI/',defaultToMainPage, name='mainPage'),
    path(r'NBI/mainPage/',defaultToMainPage, name='mainPage'),
    path(r'NBI/Image/',defaultToMainPage, name='mainPage'),
    path(r'NBI/Image/mainPage/',mainPage,name='mainPage'),

    path(r'NBI/Image/upload/', uploadImage,name='uploadImage'),
    path(r'NBI/Image/getResult/', updateInputAndGetNBI,name='inputUpdate'),
    path(r'NBI/Image/chooseLastImage/', chooseLastImage, name='chooseLastImage'),

    # """User"""
    path(r'NBI/User/',defaultToUserLoginPage, name='userPage'),
    path(r'NBI/User/loginPage/', userLoginPage,name='userLoginPage'),

    path(r"NBI/User/register/sendemail", sendValidCodeEmail, name="validCodeEmail"),
    path(r"NBI/User/register/", registerNewUser, name="registerNewUser"),
    path(r"NBI/User/checkLogin/", loginCheck, name="loginWithAccount"),
    path(r"NBI/User/checkByToken/", checkByToken, name="checkByToken"),

    # """History Info Gallery"""
]

