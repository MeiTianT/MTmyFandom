#coding=utf-8
from __future__ import unicode_literals

from django.apps import AppConfig

#app名称修改（显示为中文或想要的内容）
class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = u"用户信息"
