from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from operation.models import *
from django.http import HttpResponse
from django.db.models import Q
from collections import OrderedDict
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect

#圈子列表
class QaunListView(View):
    def get(self,request):
        # 获取所有圈子按最新排列
        all_fandom=QuanZi.objects.all().order_by("-add_time")
        # 获取所有的热门圈子按关注数排列取前3个
        hot_fandom=QuanZi.objects.all().order_by("-fav_nums")[:3]
        # 圈子搜索,通过keywords对数据库里面的数据进行搜索，GET方法获取前端传过来的keywords
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            #可通过关键词模糊搜索，filter过滤条件为：圈子名称、描述、标签、明星与关键词相关
            all_fandom=all_fandom.filter(Q(q_name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|
                                         Q(quan_tag__icontains=search_keywords)|Q(star__star__icontains=search_keywords))

        #筛选完毕后对展示数据进行统计
            fandom_num = all_fandom.count()
        # 圈子排序
        #从前端get获取排序的类型
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "new":
                all_fandom = all_fandom.order_by("-add_time")
            elif sort == "hot":
                all_fandom = all_fandom.order_by("-fav_nums")
        # 对圈子列表分页
        #注意利用pure_pagination进行分页的，
        # 传回的对象要使用object_list作为返回对象
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 6=一页需要显示的数据
        p = Paginator(all_fandom, 6, request=request)
        all_fandom = p.page(page)
        #将数据传回前端
        # #locals()可以将函数中所有变量全部传给模板。但多余变量会浪费内存
        return render(request,"fandom-list.html",{
            "all_fandom":all_fandom,
            "sort":sort,
            "hot_fandom":hot_fandom
        })

# 圈子详情
class fandomHomeView(View):
    def get(self,request,fandom_id):
        current_page="home"
        #获取当前圈子信息
        fandom=QuanZi.objects.get(id=int(fandom_id))
        #圈子点击数+1
        fandom.click_num+=1
        #存储到数据库
        fandom.save()
        #是否有关注
        has_fav=False
        #判断用户是否登录
        if request.user.is_authenticated:
            #判断用户是否关注
            if UserFavorite.objects.filter(user=request.user,fav_id=fandom.id,fav_type=4):
                has_fav = True

        #有外键关联的，可以使用 “外键.键_set.all()” 反向获取数据
        #获取当前圈子的所有视频
        all_video=fandom.video_set.all()
        all_picture=fandom.picture_set.all()
        all_activity = fandom.activity_set.all()
        return render(request,"fandom-detail-homepage.html",{
            "all_video":all_video,
            "all_picture":all_picture,
            "all_activity": all_activity,
            "fandom":fandom,
            "current_page":current_page,
            "has_fav":has_fav
        })

# 帖子列表页
class ArticleView(View):
    def get(self,request):
        # 帖子
        all_article=Article.objects.all()
        # 热门排行
        hot_article=all_article.order_by("-com_nums")[:3]

        # 帖子搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_article = all_article.filter(
                Q(title__icontains=search_keywords) | Q(summary__icontains=search_keywords)|
                Q(q_name__q_name__icontains=search_keywords))
         # 排序
        sort= request.GET.get("sort", "")
        if sort:
            if sort=="hot":
                all_article=all_article.order_by("-com_nums")
            elif sort=="new":
                all_article=all_article.order_by("-add_time")

        # 对帖子分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_article,6,request=request)
        all_article = p.page(page)
        return render(request,"article-list.html",{
            "all_article":all_article,
            "sort":sort,
            "hot_article":hot_article
        })

# 帖子详情页，评论树
class articleDetailView(View):
    def get(self,request,article_id):
        current_page = "get-article_detail"
        article=Article.objects.get(id=int(article_id))
        fandom = QuanZi.objects.get(q_name=article.q_name)
        article.click_nums += 1
        article.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=article.id, fav_type=3):
                has_fav = True

        # 通过帖子反向获取所有评论
        comment_queryset = article.articlecomment_set.all().order_by('add_time')
        # comment_set=self.getcomment(comment_queryset)

        #构造评论树数据，得到：[{ "":"","":""},{},{}]
        comment_list = []
        for comment in comment_queryset:
            if comment.parent_comment: #如果评论有父评论
                parent_id = comment.parent_comment.id
                content = comment
                comment_id = comment.id
                user=comment.user
                add_time=comment.add_time
                dict = {'add_time': add_time,'user': user, 'content': content,'id': comment_id, 'parent_id': parent_id}
                comment_list.append(dict)
            else:
                parent_id = None #没有父评论，则parent_id为None
                content = comment
                comment_id = comment.id
                user = comment.user
                add_time=comment.add_time
                dict = {'add_time': add_time,'user': user, 'content': content,'id': comment_id, 'parent_id': parent_id}
                comment_list.append(dict)

        # 放一个字典，把id提出来，并且在每一个字典中加一个"children_comment":[]键值对
        #得到：{1:{"":"","":""},2:{},3:{}}
        comment_dict = {}
        for comment in comment_list:
            comment["children_comment"] = []
            comment_dict[comment['id']] = comment



        # 原始数据
        comment1 = [
                        {'content': "我是评论A，我没有父评论", 'id': 1, 'parent_id': None},
                        {'content': "我是评论B1，我的父评论是A", 'id': 2, 'parent_id': 1},
                        {'content': "我是评论B2，我的父评论是A", 'id': 3, 'parent_id': 1},
                        {'content': "我是评论C1，我的父评论是B2", 'id': 4, 'parent_id': 3},
                        {'content': "我是评论D1，我的父评论是C1", 'id': 5, 'parent_id': 4},
                    ]
        # 转换成树形结构数据
        comment2 = [
                        {'content': "我是评论A，我没有父评论", "children_comment": [
                            {'content': "我是评论B1，我的父评论是A", "children_comment": []},
                            {'content': "我是评论B2，我的父评论是A", "children_comment": [
                                {'content': "我是评论C1，我的父评论是B2", "children_comment": [
                                    {'content': "我是评论D1，我的父评论是C1", "children_comment": []}
                                ]}
                            ]}
                        ]},
                    ]

        #找到父评论为None的存放起来        # [{ "":"","":""},{},{}]
        # 得到：[{ "":"","children_comment":[{"":"","children_comment" }]},{},{}]

        comment_tree = []
        for comment in comment_list:
            pid = comment["parent_id"]
            # 如果有父评论
            if pid:
            #找到对应的父评论，添加到其子评论列表中
                comment_dict[pid]["children_comment"].append(comment)
            #如果没有有父评论
            else:
                #则将评论存到 comment_tree列表
                comment_tree.append(comment)

        #调用构建评论树HTML的方法
        html=self.build_comments_tree(comment_tree)

        # return HttpResponse('post')
        return render(request, "article-detail.html", {
            "article": article,
            "current_page": current_page,
            "has_fav": has_fav,
            "fandom": fandom,
            "comment_queryset": comment_queryset,
            "comment_list": comment_list,
            "comment_dict": comment_dict,
            "comment_tree": comment_tree,
           # "JScomment_tree": json.dumps(JScomment_tree),
            "html":html,
        })

    #构建评论树HTML
    def build_comments_tree(self,comment_tree):
        #一棵树的HTML
        tp2='''
   
<div class="item" >
    <div class="comment">
        <div class="single_comments" style="margin-left: 0em">
            <div  id="{4}" class="col-md-11 comment-content" style="margin-bottom: 10px;">
                <strong>{1}</strong>
                <div class="entry-meta small muted">
                    <span class="name">By&nbsp;&nbsp;{0}</span>&nbsp;&nbsp;&nbsp;On&nbsp;&nbsp;
                    <em>{3}</em>
                    <button type="button" class="reply" id="btn{4}">&nbsp;&nbsp;回复</button>
                </div>
            </div>
        </div>
    </div>

    <div class="body">{2}</div>
    
</div>

'''

        html = ""
        #一个item一棵树，递归遍历所有子评论
        # [{ "":"","children_comment":[{"":""}]},{},{}]
        for item in comment_tree:
            children = item.get('children_comment')
            # 如果有子评论，继续调用自己，直到没有（递归结束条件）
            if children:
                html += tp2.format(item['user'], item['content'],
                        self.build_comments_tree(children),
                        item['add_time'],item['id'],)
            else:
                html += tp2.format(item['user'], item['content'],
                         "",
                         item['add_time'],item['id'], )
        return html

# 圈子帖子列表页
class FanArticleView(View):
    def get(self,request,fandom_id):
        current_page = "fandom_article"
        fandom=QuanZi.objects.get(id=int(fandom_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=fandom.id, fav_type=3):
                has_fav = True
        all_article=fandom.article_set.all()
        # 对帖子分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, 6, request=request)
        all_article = p.page(page)
        return render(request,"fandom-detail-article.html",{

            "fandom":fandom,
            "current_page": current_page,
            "has_fav ":has_fav,
            "all_article": all_article,

        })

# 视频列表页
class VideoView(View):
    def get(self,request):
        # 视频
        all_video=Video.objects.all()
        # 热门排行
        hot_video=all_video.order_by("-fav_nums")[:3]
        # 视频搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_video = all_video.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)|Q(q_name__q_name__icontains=search_keywords))

         # 排序
        sort= request.GET.get("sort", "")
        if sort:
            if sort=="hot":
                all_video=all_video.order_by("-fav_nums")
            elif sort=="new":
                all_video=all_video.order_by("-add_time")

        # 对视频分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_video,6,request=request)
        all_video = p.page(page)
        return render(request,"video-list.html",{
            "all_video":all_video,
            "sort":sort,
            "hot_video":hot_video
        })

# 视频详情
class VideoDetailView(View):
    def get(self,request,video_id):
        current_page="video"
        fandom_video=Video.objects.get(id=int(video_id))
        fandom_video.click_nums+=1
        fandom_video.save()
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=fandom_video.id,fav_type=1):
                has_fav = True
        all_video=fandom_video.video_set.all()
        return render(request,"video-detail-homepage.html",{
            "all_video":all_video,
            "fandom_video":fandom_video,
            "current_page":current_page,
            "has_fav":has_fav
        })

# 圈子视频列表页
class FanVideoView(View):

    def get(self,request,fandom_id):
        current_page = "fandom_video"
        fandom=QuanZi.objects.get(id=int(fandom_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=fandom.id, fav_type=1):
                has_fav = True
        fandom_all_video=fandom.video_set.all()
        # 对视频分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generatio
        p = Paginator(fandom_all_video, 6, request=request)
        all_video = p.page(page)
        return render(request,"fandom-detail-video.html",{
            "fandom_all_video":fandom_all_video,
            "fandom":fandom,
            "current_page": current_page,
            "has_fav ":has_fav,
            "all_video": all_video,

        })

# 图片列表页
class PictureView(View):
    def get(self,request):
        # 图片
        all_picture=Picture.objects.all()
        # 热门排行
        hot_picture=all_picture.order_by("-fav_nums")[:3]

        # 图片搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_picture = all_picture.filter(
                Q(name__icontains=search_keywords)|Q(q_name__q_name__icontains=search_keywords) )


         # 排序
        sort= request.GET.get("sort", "")
        if sort:
            if sort=="hot":
                all_picture=all_picture.order_by("-fav_nums")
            elif sort=="new":
                all_picture=all_picture.order_by("-add_time")

        # 对图片分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_picture,6,request=request)
        all_picture = p.page(page)
        return render(request,"picture-list.html",{
            "all_picture":all_picture,
            "sort":sort,
            "hot_picture":hot_picture
        })

# 图片详情
class PictureDetailView(View):

    def get(self,request,picture_id):
        current_page="picture"
        fandom_picture=Picture.objects.get(id=int(picture_id))
        fandom_picture.click_nums+=1
        fandom_picture.save()
        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=fandom_picture.id,fav_type=2):
                has_fav = True
        all_picture=fandom_picture.picture_set.all()
        return render(request,"picture-detail-homepage.html",{
            "all_picture":all_picture,
            "fandom_picture":fandom_picture,
            "current_page":current_page,
            "has_fav":has_fav
        })

# 圈子图片列表页
class FanPictureView(View):

    def get(self,request,fandom_id):
        current_page = "fandom_picture"
        fandom=QuanZi.objects.get(id=int(fandom_id))
        all_picture=fandom.picture_set.all()
        # 对图片分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_picture,8,request=request)
        all_picture = p.page(page)

        return render(request,"fandom-detail-picture.html",{
            "all_picture":all_picture,
            "fandom":fandom,
            "current_page": current_page,
        })

# 活动列表页
class ActivityView(View):
    def get(self,request):
        # 活动
        all_activity=Activity.objects.all()
        # 热门排行
        hot_activity=all_activity.order_by("-fav_nums")[:3]

        # 活动搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_activity = all_activity.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)| Q(a_addr__icontains=search_keywords)|Q(q_name__q_name__icontains=search_keywords))


         # 排序
        sort= request.GET.get("sort", "")
        if sort:
            if sort=="hot":
                all_activity=all_activity.order_by("-fav_nums")
            elif sort=="new":
                all_activity=all_activity.order_by("-add_time")

        # 对活动分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_activity,3,request=request)
        all_activity = p.page(page)
        return render(request,"activity-list.html",{
            "all_activity":all_activity,
            "sort":sort,
            "hot_activity":hot_activity
        })

# 活动详情
class ActivityDetailView(View):

    def get(self,request,activity_id):
        current_page="activity"
        activity=Activity.objects.get(id=int(activity_id))
        activity.click_nums+=1
        activity.save()
        return render(request,"activity-detail-homepage.html",{
            "activity":activity,
            "current_page":current_page,

        })

# 圈子活动列表页
class FanActivityView(View):
    def get(self,request,fandom_id):
        current_page = "fandom_activity"
        fandom=QuanZi.objects.get(id=int(fandom_id))
        fandom_all_activity=fandom.activity_set.all()
        # 对活动分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(fandom_all_activity, 3, request=request)
        all_activity = p.page(page)
        return render(request,"fandom-detail-activity.html",{
            "fandom_all_activity":fandom_all_activity,
            "fandom":fandom,
            "current_page": current_page,
            "all_activity": all_activity,

        })

# 用户收藏 点赞
class AddFavView(View):
    def post(self,request):
        fav_id=request.POST.get("fav_id",0)
        fav_type = request.POST.get("fav_type", 0)
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))

        if exist_records:
            # 如果记录在 表示取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                video=Video.objects.get(id=int(fav_id))
                video.fav_nums-=1
                if video.fav_nums < 0:
                    video.fav_nums = 0
                video.save()
            elif int(fav_type) == 2:
                picture=Picture.objects.get(id=int(fav_id))
                picture.fav_nums-=1
                if picture.fav_nums < 0:
                    picture.fav_nums = 0
                picture.save()
            elif int(fav_type) == 3:
                article = Article.objects.get(id=int(fav_id))
                article.fav_nums -= 1
                if article.fav_nums < 0:
                    article.fav_nums = 0
                article.save()
            elif int(fav_type) == 4:
                fandom = QuanZi.objects.get(id=int(fav_id))
                fandom.fav_nums -= 1
                if fandom.fav_nums < 0:
                    fandom.fav_nums = 0
                fandom.save()
            return HttpResponse('{"status":"cancelSuccess","msg":"取消关注！"}', content_type='application/json')
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user=request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    video = Video.objects.get(id=int(fav_id))
                    video.fav_nums += 1
                    video.save()
                elif int(fav_type) == 2:
                    picture = Picture.objects.get(id=int(fav_id))
                    picture.fav_nums += 1
                    picture.save()
                elif int(fav_type) == 3:
                    article = Article.objects.get(id=int(fav_id))
                    article.fav_nums += 1
                    article.save()
                elif int(fav_type) == 4:
                    fandom = QuanZi.objects.get(id=int(fav_id))
                    fandom.fav_nums += 1
                    fandom.save()
                return HttpResponse('{"status":"success","msg":"关注成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"关注出错！"}', content_type='application/json')







