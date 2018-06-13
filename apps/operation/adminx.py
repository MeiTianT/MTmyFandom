
import xadmin
from .models import ArticleComment,ThumbUp,UserFavorite,JoinFan,UserMessage


class TumbupAdmin(object):
    list_display = ['fav_id', 'user','date', 'thumbup_type']
    search_fields = ['user','date', 'thumbup_type']
    list_filter = ['user','date', 'thumbup_type']


class ArticleCommentsAdmin(object):
    list_display = ['user', 'article', 'parent_comment', 'comments', 'add_time']
    search_fields = ['user', 'article',  'add_time']
    list_filter = ['user', 'article', 'add_time']




class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = [ 'user','fav_id', 'fav_type', 'add_time']



class JoinFanAdmin(object):
    list_display = ['user', 'q_name', 'add_time']
    search_fields = ['user', 'q_name', 'add_time']
    list_filter = ['user', 'q_name', 'add_time']

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']



xadmin.site.register(ThumbUp,TumbupAdmin)
xadmin.site.register(ArticleComment,ArticleCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(JoinFan,JoinFanAdmin)
xadmin.site.register(UserMessage,UserFavoriteAdmin)