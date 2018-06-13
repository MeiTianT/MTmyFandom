from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# 采用继承的方式扩展用户信息
class UserProfile(AbstractUser): #继承AbstractUser等于继承auth_user数据表的类
    nick_name=models.CharField(max_length=50,verbose_name=u"昵称")
    birday=models.DateField(max_length=50,null=True,blank=True,verbose_name=u"生日")

    #choices属性，这个属性可以提供被选数据。如果一个字段设置了这个属性,
    # 在模版中如果要显示这个字段，那么django模版系统就会将它默认解析为一个下拉菜单
    gender=models.CharField(choices=(("male",u"男"),("female",u"女")),default=u"female",max_length=10)
    address=models.CharField(max_length=100,default=u"",verbose_name=u"所在城市")
    mobile=models.CharField(max_length=11,null=True,blank=True,verbose_name=u"手机号")

    #upload_to="user_head_img/%y/%m",建立以年月分开的文件夹
    image=models.ImageField(upload_to="user_head_img/%y/%m",default=u"user_head_img/df.jpg",max_length=100,verbose_name=u"头像")

    class Mate:
        verbose_name=u"用户信息"
        verbose_name_plural=verbose_name
        ordering=["-id"]

    #python2.x调用__unicode__（self）方法
    def __str__(self):
         return self.username

#邮箱验证数据表
class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name=u"验证码")
    email=models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type=models.CharField(verbose_name=u"发送类型",choices=(("register",u"注册"),("forget",u"忘记密码"),("update_email",u"修改邮箱")),max_length=50)
    send_time=models.DateTimeField(verbose_name=u"发送时间",default=datetime.now)


    class Meta:
        verbose_name=u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

#轮播图数据表
class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u"标题")
    image=models.ImageField(upload_to="banner/%y/%m",verbose_name=u"轮播图")
    url=models.URLField(max_length=200,verbose_name=u"访问地址")
    index=models.IntegerField(default=100,verbose_name=u"顺序")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Mate:
        verbose_name=u"轮播图"
        verbose_name_plural=verbose_name




