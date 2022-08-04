
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .UserManagement.register import sendValidCodeEmail, registerNewUser
from .UserManagement.login import loginCheck, checkByToken
from .ImageProcess.requestFunctions import updateInputAndGetNBI, uploadImage, chooseLastImage


urlpatterns = [
    path(r'NBI/admin/', admin.site.urls),
    path(r'NBI/', TemplateView.as_view(template_name='index.html')),

    # '''Image Process'''
    path(r'NBI/Image/upload/', uploadImage, name='uploadImage'),
    path(r'NBI/Image/getResult/', updateInputAndGetNBI, name='inputUpdate'),
    path(r'NBI/Image/chooseLastImage/', chooseLastImage, name='chooseLastImage'),

    # """User"""
    path(r"NBI/User/register/sendEmail", sendValidCodeEmail, name="validCodeEmail"),
    path(r"NBI/User/register/", registerNewUser, name="registerNewUser"),
    path(r"NBI/User/checkLogin/", loginCheck, name="loginWithAccount"),
    path(r"NBI/User/checkByToken/", checkByToken, name="checkByToken"),
]
