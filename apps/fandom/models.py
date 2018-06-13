from __future__ import unicode_literals
from datetime import datetime

from users.models import UserProfile
from django.db import models

#圈子表
class QuanZi(models.Model):
    q_name = models.CharField(max_length=50, unique=True,verbose_name=u"圈子名称")
    desc = models.CharField(max_length=140, default='未知',verbose_name=u"圈子描述")
    #desc = UEditorField(verbose_name=u"描述", width=600, height=300, imagePath="courses/ueditor/",
                        #filePath="courses/ueditor/", default='')

    star = models.ForeignKey('Star',verbose_name=u"所属明星", related_name='quanzi_star',default='', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="fandom/%y/%m", verbose_name=u"封面图", max_length=100)
    tag = models.CharField(choices=(("ys", u"影视"), ("gs", u"歌手"), ("zy", u"综艺")), max_length=2, verbose_name=u"标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")
    user = models.ForeignKey(UserProfile, verbose_name=u"圈子管理员",related_name='quanzi_user', on_delete=models.CASCADE)
    is_banner=models.BooleanField(default=False,verbose_name=u"是否轮播")
    quan_tag = models.CharField(verbose_name=u"圈子标签", default='', max_length=10)
    fav_nums = models.IntegerField(default=0, verbose_name=u"关注人数")
    click_num= models.IntegerField(default=0, verbose_name=u"点击数")

    class Meta:
        verbose_name = u"圈子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.q_name

    def get_video(self):
        # 获取所属视频
        return self.video_set.all()
    def get_nums_video(self):
        # 获取所有视频总数
        return self.video_set.all().count()
    get_nums_video.short_description="视频总数"

    def get_picture(self):
        # 获取所属图片
        return self.picture_set.all()
    def get_nums_picture(self):
        # 获取所有图片总数
        return self.picture_set.all().count()
    get_nums_picture.short_description="图片总数"

    def get_article(self):
        # 获取所属帖子
        return self.article_set.all()
    def get_nums_article(self):
        # 获取所有帖子总数
        return self.article_set.all().count()
    get_nums_article.short_description="帖子总数"

    def get_activity(self):
        # 获取所属活动
        return self.activity_set.all()
    def get_nums_activity(self):
        # 获取所有活动总数
        return self.activity_set.all().count()
    get_nums_activity.short_description="活动总数"

#明星表
class Star(models.Model):
    #tag = models.ForeignKey(QuanZi, verbose_name=u"所属标签", related_name='star_tag',on_delete=models.CASCADE)
    star = models.CharField(max_length=100, unique=True, verbose_name=u"名字")
    constellation = models.CharField(max_length=100,default='未知', verbose_name=u"星座")
    Bloodtype = models.CharField(max_length=100,default='未知', verbose_name=u"血型")
    height = models.CharField(max_length=100, default='未知',verbose_name=u"身高")
    birth = models.DateField(verbose_name=u"生日")
    birthadd = models.CharField(max_length=100,default='未知', verbose_name=u"出生地")
    himage =models.ImageField(upload_to="star_head_img/%y/%m", verbose_name=u"头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"创建时间")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    click_nums= models.IntegerField(default=0, verbose_name=u"点击数")

    class Meta:
        verbose_name = u"明星资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.star

#视频表
class Video(models.Model):
    q_name = models.ForeignKey(QuanZi, verbose_name=u"所属圈子", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,  unique=True,verbose_name=u"视频名")
    url = models.FileField(upload_to="video/%y/%m", verbose_name=u"视频内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    desc = models.CharField(max_length=300,default='未知', verbose_name=u"视频描述")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    click_nums= models.IntegerField(default=0, verbose_name=u"点击数")
    user = models.ForeignKey(UserProfile, verbose_name=u"上传人",related_name='video_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#帖子表
class Article(models.Model):
    q_name = models.ForeignKey(QuanZi, verbose_name=u"所属圈子", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, verbose_name=u"文章标题")  # 标题,唯一
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    head_img = models.ImageField(upload_to="article/%y/%m", verbose_name=u"标题图")  # 标题图片，上传图片到文件夹uploads
    summary = models.CharField(max_length=25)  # 简介
    content = models.TextField(u"内容")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"作者")
    priority = models.IntegerField(u"优先级", default=1000)  # 置顶
    com_nums = models.IntegerField(default=0, verbose_name=u"评论数")
    click_nums= models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")


    class Meta:
        verbose_name = u"帖子"
        verbose_name_plural = verbose_name

    def __str__(self):  # 默认返回值
        return "<%s, author:%s>" % (self.title, self.user)

#活动表
class Activity(models.Model):
    q_name = models.ForeignKey(QuanZi, verbose_name=u"所属圈子", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name=u"活动名")
    desc = models.CharField(max_length=300, default='未知',verbose_name=u"活动描述")
    fav_nums = models.IntegerField(default=0, verbose_name=u"加入人数")
    a_time = models.DateField(max_length=50, null=True, blank=True, verbose_name=u"活动时间")
    a_addr = models.CharField(max_length=100, default='未知',verbose_name=u"活动地点")
    image = models.ImageField(upload_to="activity/%y/%m", verbose_name=u"封面图", max_length=100)
    click_nums= models.IntegerField(default=0, verbose_name=u"点击数")


    class Meta:
        verbose_name = u"活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#图片表
class Picture(models.Model):
    q_name = models.ForeignKey(QuanZi, verbose_name=u"所属圈子", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,  unique=True,verbose_name=u"图片名")
    url = models.ImageField(upload_to="picture/%y/%m", verbose_name=u"图片内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    click_nums= models.IntegerField(default=0, verbose_name=u"点击数")
    user = models.ForeignKey(UserProfile, verbose_name=u"上传人",related_name='picture_user', on_delete=models.CASCADE)


    class Meta:
        verbose_name = u"图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#圈子轮播表
class BannerCourse(QuanZi):
    class Meta:
        verbose_name=u"轮播圈子"
        verbose_name_plural=verbose_name
        # 不再生成一张表 但是具有QuanZi的功能
        proxy=True
