from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .userManagement.register import sendValidCodeEmail, registerNewUser
from .userManagement.login import loginCheck, checkByToken, logoutCheck
from .userManagement.userCenterFunctions import getUserInfo, updateNewUName, updateNewAddInfo, checkInviteCode, updateNewPwd
from .ImageProcess.requestFunctions import updateInputAndGetNBI, uploadImage, chooseLastImage, historyImgInfo
from .historyManagement.history import historyDisplay, deleteHistoryImage

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
    path(r"NBI/User/logout/", logoutCheck, name="logout"),
    path(r"NBI/User/checkByToken/", checkByToken, name="checkByToken"),
    path(r"NBI/User/getUserInfo/", getUserInfo, name="getUserInfoByToken"),
    path(r"NBI/User/uploadNewUName/", updateNewUName),
    path(r"NBI/User/uploadNewAddInfo/", updateNewAddInfo),
    path(r"NBI/User/uploadNewPwd/", updateNewPwd),
    path(r"NBI/User/inputInviteCode/", checkInviteCode),

    # """History Data"""
    path(r"NBI/History/display/", historyDisplay, name="historyDisplay"),
    path(r'NBI/HistoryDetail/', historyImgInfo, name="HistoryImgInfo"),
    path(r'NBI/History/DeleteImage/', deleteHistoryImage, name="deleteOneImage")
]
