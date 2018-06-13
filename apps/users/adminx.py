
import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner,UserProfile
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import User

# 基本的修改
class BaseSetting(object):
    enable_themes=True # 打开主题功能
    use_bootswatch=True

# 针对全局的
class GlobalSettings(object):
    site_title="饭友圈后台管理系统"  # 系统名称
    site_footer="饭友圈在线网"  # 底部版权栏
    menu_style="accordion"  # 将菜单栏收起来

class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']
    model_icon = 'fa fa-group'

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

class UserProfileAdmin(UserAdmin):
    pass

# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)



