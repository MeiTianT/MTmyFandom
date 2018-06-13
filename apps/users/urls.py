
from django.conf.urls import url,include
from .views import *

app_name = 'users'
urlpatterns = [
    # 用户信息页
    url(r'^info/', UserInfoView.as_view(),name="user_info"),
    # 用户上传头像
    url(r'^image/upload/$', UpLoadImageView.as_view(),name="image_upload"),
    # 个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(),name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdataEmailView.as_view(), name="update_email"),

    # 我的圈子
    url(r'^myfav/fandom/$', MyFavFanView.as_view(), name="myfav_fandom"),

    # 我收藏的视频
    url(r'^myfav/video/$', MyFavVidView.as_view(), name= "myfav_video"),
    # 我收藏的图片
    url(r'^myfav/picture/$', MyFavPicView.as_view(), name= "myfav_picture"),
    # 我收藏的帖子
    url(r'^myfav/article/$', MyFavArtView.as_view(), name= "myfav_article"),

    # 我发表的视频
    url(r'^mypo/video/$', MyPoVidView.as_view(), name="mypo_video"),
    # 我发表的图片
    url(r'^mypo/picture/$', MyPoPicView.as_view(), name="mypo_picture"),
    # 我发表的帖子
    url(r'^mypo/article/$', MyPoArtView.as_view(), name="mypo_article"),
    # 我发表的评论
    url(r'^mypo/comment/$', MyPoComView.as_view(), name="mypo_comment"),
    #删除发表
    url(r'^del_po/$', DelPoView.as_view(), name="del_po"),


    #上传帖子
    url(r'^new/article/(?P<fandom_id>\d+)/$', newArticleView.as_view(), name="new_article"),
    #上传视频
    url(r'^new/video/(?P<fandom_id>\d+)/$', newVideoView.as_view(), name="new_video"),
    # 上传图片
    url(r'^new/picture/(?P<fandom_id>\d+)/$', newPictureView.as_view(), name="new_picture"),

    # 发表评论
    url(r'^new/comment/(?P<article_id>\d+)/$', newCommentView.as_view(), name="new_comment"),

    # 回复评论
    url(r'^reply/comment/(?P<comment_id>\d+)/$', replyCommentView.as_view(), name="reply"),

    url(r'^p1',p1View.as_view(), name="p1"),
    url(r'^p2',p2View.as_view(), name="p2"),

]
