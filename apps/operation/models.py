#coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models


from users.models import UserProfile
from fandom.models import QuanZi
# Create your models here.

from fandom.models import  Article
from datetime import datetime

#帖子评论表
class ArticleComment(models.Model):
    # 一对多，一个帖子多条评论，一条评论只属于一个帖子
    user=models.ForeignKey(UserProfile,verbose_name=u"用户",on_delete=models.CASCADE)
    article=models.ForeignKey(Article,verbose_name=u"帖子",on_delete=models.CASCADE)
    #父评论，关联自己,加上related_name='p_comment'才不会和自己冲突
    # parent_comment = models.ForeignKey('ArticleComment',)
    parent_comment = models.ForeignKey('self',related_name='p_comment',verbose_name=u"父评论",blank=True,null=True,on_delete=models.CASCADE)
    comments=models.TextField(max_length=200,verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    def __str__(self):
        return self.comments
    class Meta:
        verbose_name = u"帖子评论"
        verbose_name_plural = verbose_name

#收藏表
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    fav_id=models.IntegerField(default=0,verbose_name=u"数据id")
    fav_type=models.IntegerField(choices=((1,"视频"),(2,"图片"),(3,"帖子"),(4,"圈子")),default=1,verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class ThumbUp(models.Model):
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    thumbup_type=models.IntegerField(choices=((1,"视频"),(2,"图片"),(3,"帖子")),default=1,verbose_name=u"点赞类型")
    def __str__(self):
        return "<user:%s>" %(self.user)

    class Meta:
        verbose_name='点赞'
        verbose_name_plural = verbose_name
class JoinFan(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    q_name = models.ForeignKey(QuanZi, verbose_name=u"圈子",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"关注圈子"
        verbose_name_plural = verbose_name
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name










