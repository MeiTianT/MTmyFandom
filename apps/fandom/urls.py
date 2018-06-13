
from django.conf.urls import url
from .views import *

app_name = 'fandom'

urlpatterns = [
    # 圈子列表页
    url(r'^list/', QaunListView.as_view(),name="fandom_list"),
    # 圈子详情页
    url(r'^home/(?P<fandom_id>\d+)/$', fandomHomeView.as_view(),name="fandom_home"),
    # 圈子视频
    url(r'^fandom_video/(?P<fandom_id>\d+)/$', FanVideoView.as_view(), name="fandom_video"),
    # 圈子图片
    url(r'^fandom_picture/(?P<fandom_id>\d+)/$', FanPictureView.as_view(), name="fandom_picture"),
    # 圈子帖子
    url(r'^fandom_article/(?P<fandom_id>\d+)/$', FanArticleView.as_view(), name="fandom_article"),
    # 圈子活动
    url(r'^fandom_activity/(?P<fandom_id>\d+)/$', FanActivityView.as_view(), name="fandom_activity"),

    # 帖子列表页
    url(r'^article/list/', ArticleView.as_view(), name="article_list"),
    # 帖子详情页
    url(r'^article/detail/(?P<article_id>\d+)/$', articleDetailView.as_view(), name="article_detail"),

    # 视频列表页
    url(r'^video/list/', VideoView.as_view(), name="video_list"),
    # 视频详情页
    url(r'^video/detail/(?P<video_id>\d+)/$', VideoDetailView.as_view(), name="video_detail"),

    # 图片列表页
    url(r'^picture/list/', PictureView.as_view(), name="picture_list"),
    # 图片详情页
    url(r'^picture/detail/(?P<picture_id>\d+)/$', PictureDetailView.as_view(), name="picture_detail"),

    # 活动列表页
    url(r'^activity/list/', ActivityView.as_view(), name="activity_list"),
    # 活动详情页
    url(r'^activity/detail/(?P<activity_id>\d+)/$', ActivityDetailView.as_view(), name="activity_detail"),

    # 添加收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]
