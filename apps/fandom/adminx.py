
import xadmin
from .models import Star,QuanZi,Picture,Video,Article,Activity,BannerCourse

#圈子管理
class QuanAdmin(object):
    # 查看
    list_display=['q_name','desc','star','fav_nums','image','tag','add_time','user','quan_tag','click_num','get_nums_video']
    # 查找
    search_fields=['q_name','star','tag','add_time','user','quan_tag']
    # 过滤,要在过滤条件中显示外键的子内容时，用双下划线,格式：外键__子内容
    list_filter=['q_name','star','fav_nums','tag','add_time','user','quan_tag','click_num',]
    # 根据点击数排列
    ordering=['-click_num']
    # 只读
    readonly_fields=['click_num','fav_nums','add_time']
    # 在列表页直接修改
    list_editable=['tag','desc','image','quan_tag']

    # 自动刷新页面 3，5表示秒数
    refresh_times = [3,5]
    # 指明圈子中desc字段 用富文本编辑
    style_fields={"desc":"ueditor"}
    import_excel = True

    def save_models(self):
        # 在保存圈子的时候统计圈子数
        obj=self.new_obj
        obj.save()
        if obj.star is not None:
            quanzi_star=obj.star
            quanzi_star.quanzi_nums=QuanZi.objects.filter(star=quanzi_star).count()
            quanzi_star.save()

    def queryset(self):
        qs = super(QuanAdmin, self).queryset()
        qs = qs.filter(is_banner=False)  ####
        return qs

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(QuanAdmin, self).post(request, args, kwargs)

#banner管理
class BannerCourseAdmin(object):
    # 查看
    list_display=['q_name','desc','star','fav_nums','image','tag','add_time','user','quan_tag','click_num',]
    # 查找
    search_fields=['q_name','star','tag','add_time','user','quan_tag']
    # 过滤
    list_filter=['q_name','star','fav_nums','tag','add_time','user','quan_tag','click_num',]
    # 根据点击数排列
    ordering=['-click_num']
    # 只读
    readonly_fields=['click_num','fav_nums','add_time']

    def queryset(self):
        qs=super(BannerCourseAdmin,self).queryset()
        qs=qs.filter(is_banner=True)  ###
        return qs

#明星管理
class StarAdmin(object):
    # 查看
    list_display=['star','constellation','Bloodtype','height','birth','birthadd','himage','add_time','fav_nums']
    # 查找
    search_fields=['star','fav_nums','add_time']
    # 过滤
    list_filter=['star','fav_nums','add_time']
    # 只读
    readonly_fields=['fav_nums','add_time']
    # 在列表页直接修改
    list_editable=['constellation','Bloodtype','height','birth','birthadd','himage']

#图片管理
class PictureAdmin(object):
    # 查看
    list_display=['q_name','name','url','add_time','fav_nums',]
    # 查找
    search_fields=['q_name','name','add_time','fav_nums',]
    # 过滤
    list_filter=['q_name','name','add_time','fav_nums',]
    # 根据点击数排列
    ordering=['-fav_nums']
    # 只读
    readonly_fields=['fav_nums','add_time']
    # 在列表页直接修改
    list_editable=['name','url']

#帖子管理
class ArticleAdmin(object):
    # 查看
    list_display=['q_name','title','head_img','summary','add_time','user','com_nums','priority',]
    # 查找
    search_fields=['q_name','title','user','add_time','com_nums','priority',]
    # 过滤
    list_filter=['q_name','title','user','add_time','com_nums','priority',]
    # 根据点击数排列
    ordering=['-com_nums']
    # 只读
    readonly_fields=['com_nums','add_time']
    # 在列表页直接修改
    list_editable=['title','head_img','summary','priority']

    # 自动刷新页面 3，5表示秒数
    refresh_times = [3,5]

#活动管理
class ActivityAdmin(object):
    # 查看
    list_display=['q_name','name','desc','a_time','fav_nums','image']
    # 查找
    search_fields=['q_name','name','a_time','fav_nums',]
    # 过滤
    list_filter=['q_name','name','a_time','fav_nums',]
    # 根据点击数排列
    ordering=['-fav_nums']
    # 只读
    readonly_fields=['fav_nums']
    # 在列表页直接修改
    list_editable=['name','desc','image']

#视频管理
class VideoAdmin(object):
    # 查看
    list_display=['q_name','name','url','add_time','fav_nums','desc']
    # 查找
    search_fields=['q_name','name','add_time','fav_nums',]
    # 过滤
    list_filter=['q_name','name','add_time','fav_nums',]
    # 根据点击数排列
    ordering=['-fav_nums']
    # 只读
    readonly_fields=['add_time','fav_nums']
    # 在列表页直接修改
    list_editable=['name','desc','url',]

#注册admin
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(QuanZi,QuanAdmin)
xadmin.site.register(Star,StarAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(Picture,PictureAdmin)
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Activity,ActivityAdmin)




