
#三种类型的邮件
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord

from myFandom.settings import EMAIL_FROM

# 产生随机验证码，长度可调
def random_str(randomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length=len(chars)-1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

# 发送邮件
def send_register_email(email,send_type="register"):
    ###########################生成随机验证码存入数据库中###########################
    email_record=EmailVerifyRecord()  #继承模型
    if send_type == "update_email":
        code=random_str(4)
    else:
        code=random_str(16)

    # 将随机生成code存入数据库中
    email_record.code=code
    # 将管理的邮箱传入数据库中
    email_record.email=email
    # 定义发送类型
    email_record.send_type=send_type
    email_record.save()  # 保存到数据库

    ###########################发送激活邮件###########################
    email_title=""
    email_body=""

    if send_type=="register":
        email_title = "饭友圈网激活链接"
        email_body = "  请点击下面的链接激活你的帐号:http://127.0.0.1:8000/active/{0}".format(code)

    if send_type=="forget":
        email_title = "饭友圈网密码重置链接"
        email_body = "  请点击下面的链接重置密码:http://127.0.0.1:8000/reset/{0}".format(code)

    if send_type == "update_email":
        email_title = "饭友圈网在线邮箱修改验证码"
        email_body = "  你的邮箱验证码为:{0}".format(code)

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass



