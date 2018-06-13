from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView
import xadmin
from users.views import IndexView

from users.views import *
from users import views

from myFandom.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^login/$', LoginView.as_view(),
        name="login"),  # 登录

    url(r'^$', IndexView.as_view(),name="index"),#首页
    url(r'^xadmin/', xadmin.site.urls),#管理后台
    url(r'^logout/$', LogOutView.as_view(),name="logout"),#登出
    url(r'^register/$',  RegisterView.as_view(),name="register"),#注册
    url(r'^captcha/', include('captcha.urls')),#验证码

    #通过(?P.*？)正则获取获取匹配的字符串（实际就是发送的验证码），
    # 绑定ActiveUserView，通过该类完成激活
    url(r'^active/(?P<active_code>.*?)/$', ActiveUserView.as_view(), name="ActiveUserView"),
    url(r'^forget/$', ForgetPwdView.as_view(),name="ForgetPwdView"),#忘记密码
    url(r'^reset/(?P<active_code>.*?)/$', ResetView.as_view(),name="ResetView"),#重置密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(),name="ModifyPwdView"),#更改密码

    # 圈子相关URL配置
    url(r'^fandom/', include('fandom.urls')),
    # 用户相关URL配置
    url(r'^users/', include('users.urls')),
    # 用户操作相关URL配置
    url(r'^operation/', include('operation.urls')),
    # 配置上传文件访问处理函数
    url(r'^media/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),
    # 富文本相关URL
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    # url(r'^static/(?P<path>.*)$', serve,{"document_root":STATIC_ROOT}),
]
#全局404 500 页面配置
# (放ViewS的路径)
handler404='users.views.page_not_found'
handler500='users.views.page_error'

urlpatterns += staticfiles_urlpatterns()