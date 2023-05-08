import json

from django.http import HttpResponse
from django.template import loader
import random
import smtplib
from email.mime.text import MIMEText
from .md5 import transToMD5
from ..dataManagement.dbFunction import checkUIDRegistered
from ..dataManagement.db_User import User
from ..dataManagement.db_ValidateCode import ValidateCode, checkValidateCode


# 发送带验证码邮件到指定邮箱，同时返回验证码到前端
def sendValidCodeEmail(request):
    body = json.loads(request.body.decode('utf-8'))
    email = body["email"]
    code = getEmailcode()
    sendResult = sendEmail(code=code, target=email)
    if sendResult:
        # 记录该验证码置db
        validateCode = ValidateCode(email, code)
        validateCode.saveNewValidateCode()
        return HttpResponse(1)
    else:
        return HttpResponse(2)


# 邮箱验证码
def getEmailcode():
    ret = ''
    for i in range(6):
        ret += str(random.randint(0, 9))
    return ret


# 发送验证邮件
def sendEmail(code, target):
    mail_user = "nbi_online@163.com"
    mail_password = "BNYNKQWZHZTHNIJS"
    mail_from = "NBI_Online"
    # 加载模板
    template = loader.get_template('part_email.html')
    # 渲染模板
    mail_content = template.render({"validateCode": code})
    mail_host = "smtp.163.com"

    msg = MIMEText(mail_content, "html", "utf-8")
    msg['Subject'] = "NBI Online注册验证码（无需回复）"
    me = mail_from + "<" + mail_user + ">"
    msg['From'] = me
    msg['To'] = target

    try:
        server = smtplib.SMTP(port=19999)
        server.connect(mail_host)
        server.login(mail_user, mail_password)
        server.sendmail(me, target, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


# 注册新用户
def registerNewUser(request):
    body = json.loads(request.body.decode('utf-8'))
    print(body)
    emailAddress = body["email"]
    upw = transToMD5(str(body["pw"]))
    vcode = body['vcode']
    # 检查这个用户是否已经注册
    if checkUIDRegistered(emailAddress):
        # 0表示该账户已被注册
        return HttpResponse(0)

    # 检查验证码
    vCodeCheck = checkValidateCode(emailAddress, vcode)
    if vCodeCheck != 0:
        # 不等于0表示验证码检查失败
        return HttpResponse(vCodeCheck)

    # 创建新用户
    newUser = User(uid=emailAddress, pwd=upw)
    newUser.saveNewUser()
    # 1表示注册成功
    return HttpResponse(1)
