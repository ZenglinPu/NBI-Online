from django.http import HttpResponse
from django.template import loader
import random
import smtplib
from email.mime.text import MIMEText
from NBI.UserManagement.md5 import transToMD5
from NBI.dataManagement.db_User import User
from NBI.dataManagement.dbFunction import checkUIDRegistered

# 发送带验证码邮件到指定邮箱，同时返回验证码到前端
# TODO: 这个需要服务器端设置好才行，目前我本地测试是可以完成邮件发送的
def sendValidCodeEmail(request):
    email = request.POST.get("email")
    code = getEmailcode()
    # sendEmail(code=code, target=email)
    return HttpResponse("邮件已发送！")

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
    mail_content = template.render({"link": code})
    mail_host="smtp.163.com"

    msg=MIMEText(mail_content,"html","utf-8")    
    msg['Subject']="NBI Online注册验证码（无需回复）"
    me=mail_from+"<"+mail_user+">"
    msg['From']=me
    msg['To']= target

    try:
        server=smtplib.SMTP(port=19999)
        server.connect(mail_host)
        server.login(mail_user,mail_password)
        server.sendmail(me,target,msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False

# 注册新用户
def registerNewUser(request):
    emailAddress = request.POST.get("email")
    upw = transToMD5(str(request.POST.get("pw")))
    # 检查这个用户是否已经注册
    if checkUIDRegistered(emailAddress):
        # 0表示该账户已被注册
        return HttpResponse(0)

    # 创建新用户
    newUser = User(uid=emailAddress, pwd=upw)
    newUser.saveNewUser()
    # 1表示注册成功
    return HttpResponse(1)