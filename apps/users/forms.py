
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile
from django.forms import fields
# 设置一些规则，验证从前台传来的表单是否合法
# 产生的错误信息存放于_errors中，在前台可查看

#登录表单
class LoginForm(forms.Form):
    # 字段名称一定要与前台的name对应
    username=forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)

#注册表单
class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

#找回密码表单
class ForgetForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

#更改密码表单
class ModifyPwdForm(forms.Form):
    password1=forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)

#上传头像表单
class UpLoadImageForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']


#用户信息表单
class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['nick_name','gender','birday','address','mobile']

#发表帖子表单
class newArticleForm(forms.Form):
    title = forms.CharField(max_length=255,min_length=5)
    summary  = forms.CharField(max_length=255,min_length=5)
    head_img = forms.ImageField()
    content = forms.CharField(min_length=10)

#发表视频表单
class newVideoForm(forms.Form):
    name = forms.CharField(max_length=15,min_length=3)
    desc  = forms.CharField(max_length=25,min_length=5)
    url= forms.FileField()
    #url = fields.FileField()

#发表图片表单
class newPictureForm(forms.Form):
    name = forms.CharField(max_length=255,min_length=5)
    url = forms.ImageField()

#发表评论表单
class newCommentForm(forms.Form):
    comment = forms.CharField(max_length=255,min_length=5)

#回复评论表单
class replyForm(forms.Form):
    new_reply = forms.CharField(max_length=255,min_length=5)

