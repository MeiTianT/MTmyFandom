import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import *
from fandom.models import Article,QuanZi
from operation.models import  ArticleComment
from django.db.models import Q
from collections import OrderedDict

from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from .forms import *
from utils.email_send import send_register_email ###


from utils.mixin_utils import LoginRequiredMixin

from operation.models import JoinFan,UserFavorite,UserMessage

from fandom.models import QuanZi,Video,Picture,Article
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from . import  models,forms

from django.views.decorators.csrf import csrf_exempt,csrf_protect

#重置密码
class ResetView(View):
    #从前端连接url获取参数验证码
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                #如果验证码正确，则跳转到重置页面
                email=record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"active_fail.html")
        #重置密码后回到登录界面
        return render(request,"login.html")

#在个人中心更改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
           pwd1=request.POST.get("password1","")
           pwd2= request.POST.get("password2", "")
           email=request.POST.get("email","")
           if pwd1 !=pwd2 :
               return render(request, "password_reset.html", {"email": email,"msg":"密码不一致"})
           user = UserProfile.objects.get(email=email)
           #加密密码
           user.password=make_password(pwd2)
           user.save()
           #更改密码后跳转回登录页面
           return render(request,"login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": "email","modify_form":modify_form})

# 找回密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form=ForgetForm()
        # 将验证码传递给前端
        return render(request,"forgetpwd.html",{"forget_form":forget_form})
    def post(self,request):
        # 验证合法
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            # post数据成功，将验证码保存在EmailVerifyCode，
            # 用于激活查询，并跳转至index页面
            email=request.POST.get("email","")
            send_register_email(email, send_type="forget")
            return render(request,"send_success.html",{"email":email})
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})

#用户激活，原理：通过get，获取激活的请求验证码，通过验证码在
# EmailVerifyRecord中查询到对应的邮箱，通过邮箱在UserProfile
# 查询到对应的账号信息，并将is_active 变为True，即完成激活
class ActiveUserView(View):
    def get(self,request,active_code): #get获取前端url传过来的请求验证码
        #查询验证码对应邮箱的记录
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                # 找到UserProfile中的对应账号
                user=UserProfile.objects.get(email=email)
                user.is_active=True #激活账号
                user.save()
        else:
            return render(request,"active_fail.html") #找不到记录则返回连接失效的页面
        return render(request,"login.html")

#邮箱登陆
class CustomBackend(ModelBackend):
    # 传入两个关键词参数
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 存在数据库的用户名是加密的，所以不能get
            # 通过user中的check_password()方法，检测密码是否正确
            if user.check_password(password):
                # 用户名密码正确，返回user对象
                return user
         # 如果get不到数据，或者多个数据，就返回异常
        except Exception as e:
            return  None

# 用户注册
class RegisterView(View):

    def get(self, request):
        #将form加入RegisterView视图中，并将form数据传入Template中
        register_form=RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST) # #将post上来的数据传递给RegisterForm
        if register_form.is_valid(): #上传的数据符合form表要求，有效
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(email=user_name):
                # 该逻辑用户判断用户是否已注册存在
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile=UserProfile()
            # 注册的时候需要查看邮箱是否有重复,利用了username进行了去重
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False #表面用户还未激活
            # 明文数据需要经过加密后传入数据库,利用make_password方法加密
            user_profile.password=make_password(pass_word)
            user_profile.save()#存储到数据库
            # 写入欢迎注册消息
            user_message=UserMessage()
            user_message.user=user_profile.id
            user_message.message="欢迎注册饭友圈在线网"
            user_message.save()
            #发送注册验证码到邮箱，用于邮件激活操作
            send_register_email(user_name,"register")
            return render(request, "send_success.html",{"email":user_name})
            #return render(request, "login.html")
        else:
            # 将register_form数据传递给Template
            return render(request, "register.html",{'register_form':register_form})

# 用户登出
class LogOutView(View):
    def get(self,request):

        if request.method == 'GET':
            ##################加入重定向至来时页面函数#################
            # 已经在来时页面埋点，将来时页面埋点在参数next中
            next_page = request.GET.get('next', '/')
        logout(request)#利用系统logout函数清除request的登陆信息
        return HttpResponseRedirect(next_page)  # 转到来时页面
        #return HttpResponseRedirect(reverse(next_page))

# 用户名登录
class LoginView(View):
    def get(self,request):
        ##################加入重定向至来时页面函数#################
        # 已经在来时页面埋点，将来时页面埋点在参数next中
        next_page = request.GET.get('next', '')
        ###########################################################
        return render(request, "login.html",{'next_page':next_page})#将next_page返回给html页面，进行埋点传值给POST
    def post(self,request):
        login_form=LoginForm(request.POST)
        #返回报错值，有报错则valid为False，没报错则为True，减少服务器查询压力
        if login_form.is_valid():
            #获取页面post上来的用户名和密码
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            #利用authenticate方法对用户信息进行校验
            user = authenticate(username=user_name, password=pass_word)
            #正确返回user对象，错误返回None
            if user is not None:
                if user.is_active:
                    # 调用login函数，实现对request进行操作，将用户信息、
                    # session、cookies等写入了request中，再用render将request进行返回
                    login(request, user)
                    #################获取html中的隐藏字段next_page#################
                    next_page = request.POST.get('next_page', '')
                    return HttpResponseRedirect(next_page)  # 转到来时页面
                   # return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户没有激活！"})
            else:
                # 通过了form表单的验证，但是账号密码不正确时
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            # form表单验证不通过，返回表单错误信息
            # 直接传入login_form，在Template里面调用error值
            return render(request, "login.html", {"login_form":login_form})


#用户个人中心
class UserInfoView(View):

    def get(self,request):
        return render(request,"usercenter-info.html",{
        })
    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

# 上传头像
class UpLoadImageView(View):
    def post(self,request):
        image_form=UpLoadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

# 个人中心修改密码
class UpdatePwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
           pwd1=request.POST.get("password1","")
           pwd2= request.POST.get("password2", "")
           if pwd1 !=pwd2 :
               return HttpResponse('{"status":"success","msg":"密码不一致"}', content_type='application/json')
           user = request.user
           user.password=make_password(pwd2)
           user.save()
           return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email=request.GET.get("email","")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email,"update_email")
        return HttpResponse('{"email":"验证码已发送至邮箱"}', content_type='application/json')

#更新邮箱
class UpdataEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_records=EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user=request.user
            user.email=email
            user.save()
            return HttpResponse('{"email":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

# 我收藏的视频
class MyFavVidView(LoginRequiredMixin,View):
    def get(self,request):
        video_list=[]
        fav_video=UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_video in fav_video:
            video_id=fav_video.fav_id
            video=Video.objects.get(id=int(video_id))
            video_list.append(video)

        return render(request,"usercenter-fav-video.html",{
            "video_list":video_list

        })

# 我收藏的图片
class MyFavPicView(LoginRequiredMixin,View):
    def get(self,request):
        picture_list=[]
        fav_picture=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_picture in fav_picture:
            picture_id=fav_picture.fav_id
            picture=Picture.objects.get(id=int(picture_id))
            picture_list.append(picture)

        return render(request,"usercenter-fav-picture.html",{
            "picture_list":picture_list

        })

# 我收藏的帖子
class MyFavArtView(LoginRequiredMixin,View):
    def get(self,request):
        article_list=[]
        fav_article=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_article in fav_article:
            article_id=fav_article.fav_id
            article=Article.objects.get(id=article_id)
            article_list.append(article)

        return render(request,"usercenter-fav-article.html",{
            "article_list":article_list

        })

# 我关注的圈子
class MyFavFanView(LoginRequiredMixin,View):
    def get(self,request):
        fandom_list=[]
        fav_fandom=UserFavorite.objects.filter(user=request.user,fav_type=4)
        for fav_fandom in fav_fandom:
            fandom_id=fav_fandom.fav_id
            fandom=QuanZi.objects.get(id=fandom_id)
            fandom_list.append(fandom)

        return render(request,"usercenter-fav-fandom.html",{
            "fandom_list":fandom_list

        })

# 我发表的视频
class MyPoVidView(LoginRequiredMixin, View):
    def get(self, request):
        po_video = Video.objects.filter(user=request.user)
        return render(request, "usercenter-po-video.html", {
                "po_video": po_video

            })

# 我发表的图片
class MyPoPicView(LoginRequiredMixin, View):
    def get(self, request):
        po_picture = Picture.objects.filter(user=request.user)
        return render(request, "usercenter-po-picture.html", {
                "po_picture": po_picture

            })

# 我发表的帖子
class MyPoArtView(LoginRequiredMixin, View):
    def get(self, request):
        po_article = Article.objects.filter(user=request.user)
        return render(request, "usercenter-po-article.html", {
            "po_article": po_article

        })

# 我发表的评论
class MyPoComView(LoginRequiredMixin, View):
    def get(self, request):
        po_comment = ArticleComment.objects.filter(user=request.user)
        return render(request, "usercenter-po-comment.html", {
                "po_comment": po_comment
            })

# 删除我的发表
class DelPoView(LoginRequiredMixin, View):
            def get(self, request):
                po_article = Article.objects.filter(user=request.user)
                return render(request, "usercenter-po-article.html", {
                    "po_article": po_article

                })

# 饭友圈首页
class IndexView(View):
    def get(self,request):
        # 取出轮播图
        all_banners=Banner.objects.all().order_by('index')
        fandom=QuanZi.objects.filter(is_banner=False)[:4]
        banner_fandom=QuanZi.objects.filter(is_banner=False)[:3]
        fandom_b15=QuanZi.objects.all()[:15]

        return render(request,"index.html",{
            "all_banners":all_banners,
            "fandom":fandom,
            "banner_fandom":banner_fandom,
            "fandom_b15":fandom_b15


        })

# 全局配置404
# 最后需要将settings的DEBUG改为FALSE，404时才会调用执行我们的404函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code=404  # 这个状态码会影响浏览器的显示
    return response

# 全局配置500
def page_errror(request):
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code=500
    return response

#发表帖子
class newArticleView(View):
    #没有这个方法会出现405错误
    @csrf_exempt
    def get(self,request,fandom_id):
        fandom=QuanZi.objects.get(id=int(fandom_id))
        newArticle_form=newArticleForm(request.GET,request.FILES)
        return render(request, "new_article.html",{
            "newArticle_form":newArticle_form,
            "fandom": fandom,
        })
    @csrf_exempt
    def post(self,request,fandom_id):
        newArticle_form=newArticleForm(request.POST,request.FILES)
        fandom=QuanZi.objects.get(id=int(fandom_id))
        if newArticle_form.is_valid():
            title = request.POST.get("title","")
            summary= request.POST.get("summary","")
            content = request.POST.get("content","")
            head_img = request.FILES.get("head_img", "")

            article=Article()
            article.title=title
            article.summary=summary
            article.content=content
            article.head_img=head_img
            article.user=request.user
            article.q_name=fandom
            article.save()
            return HttpResponse('发布成功!')
        else:
            return render(request, "new_article.html",{
                "newArticle_form":newArticle_form,
                "fandom":fandom,
                                                       })

#上传视频
class newVideoView(View):
    #没有这个方法会出现405错误
    def get(self,request,fandom_id):
        return render(request, "fandom-detail-video.html",{
        })
    @csrf_exempt
    def post(self,request,fandom_id):
        newVideo_form=newVideoForm(request.POST,request.FILES)
        fandom=QuanZi.objects.get(id=int(fandom_id))
        print (newVideo_form)

        if newVideo_form.is_valid():
            name = request.POST.get("name","")
            desc= request.POST.get("desc","")
            url = request.FILES.get("url", "")
            #url = obj.cleaned_data['url']

            video=Video()
            video.name=name
            video.desc=desc
            video.url=url
            video.user=request.user
            video.q_name=fandom
            video.save()
            target_url = '/fandom/fandom_video/'+fandom_id

            return HttpResponseRedirect(target_url)
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

#上传图片
class newPictureView(View):
    #没有这个方法会出现405错误
    def get(self,request,fandom_id):

        next_page = request.POST.get('next', '')
        #return HttpResponseRedirect(next_page)  # 转到来时页面
        #return render(request, 'fandom-detail-picture.html', {'next_page': next_page})  # 将next_page返回给html页面，进行埋点传值给POST
        return HttpResponse(json.dumps({'result':'reply get successfully'})) #JsonResponse




    @csrf_exempt
    def post(self,request,fandom_id):
        newPicture_form=newPictureForm(request.POST,request.FILES)
        fandom=QuanZi.objects.get(id=int(fandom_id))

        if newPicture_form.is_valid():
            name = request.POST.get("name","")
            url = request.FILES.get("url", "")

            picture=Picture()
            picture.name=name
            picture.url=url
            picture.user=request.user
            picture.q_name=fandom
            picture.save()
            #target_url = '/fandom/fandom_picture/'+fandom_id
            next_page = request.POST.get('next_page', '')
            #return HttpResponseRedirect(next_page)  # 转到来时页面
            #return HttpResponseRedirect(target_url)
            result = 'reply post successfully'
            return HttpResponse(json.dumps({'result': result}))
        else:
            result = 'reply post successfully but save fail'
            return HttpResponse(json.dumps({'result': result}))

#发表评论
class newCommentView(View):
    @csrf_exempt
    def get(self,request,article_id):
        result = 'successfully'
        return HttpResponse(json.dumps({'result': result}))
    @csrf_exempt
    def post(self, request, article_id):
            newComment_form = newCommentForm(request.POST, request.FILES)
            article = Article.objects.get(id=int(article_id))
            if newComment_form.is_valid():
                newcomment = request.POST.get("comment", "")
                if len(newcomment) < 5:
                    result = u'评论数需大于5'
                    return HttpResponse(json.dumps({'result': result}))
                else:
                    comment=ArticleComment()
                    comment.comments = newcomment
                    comment.user = request.user
                    comment.article =article
                    comment.save()

                    #return HttpResponse("发布成功")  # 最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
                    return HttpResponse(json.dumps({'result': "successfully"}))
            else:
                return HttpResponse(json.dumps({'result': "fail"}))

#回复评论
class replyCommentView(View):
    @csrf_exempt
    def get(self,request,comment_id):
        result = 'reply get successfully'
        return HttpResponse(json.dumps({'result': result}))
    @csrf_exempt
    def post(self, request, comment_id):
        reply_form = replyForm(request.POST, request.FILES)
        parent_comment = ArticleComment.objects.get(id=int(comment_id))
        if reply_form.is_valid():
            new_reply = request.POST.get("new_reply", "")
            if len(new_reply) < 5:
                result = '评论数需大于5'
                return HttpResponse(json.dumps({'result': result}))
            else:
                comment = ArticleComment()
                comment.comments = new_reply
                comment.parent_comment = parent_comment
                comment.user = request.user
                comment.article = parent_comment.article
                comment.save()
                result = 'reply post successfully'
                #return HttpResponse("回复成功")  # 最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
                return HttpResponse(json.dumps({'result': result}))
        else:
            result = 'reply post successfully but save fail'
            return HttpResponse(json.dumps({'result': result}))






class p1View(View):
    def get(self,request):
        return render(request, "p1.html")
class p2View(View):
    def get(self,request):
        return render(request, "p2.html")
    def post(self,request):
            city = request.POST.get("city")
            print(city)
            return render(request, "popup_response.html", {"city": city})


