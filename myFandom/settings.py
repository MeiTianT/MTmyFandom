
import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

######注意这里：将文件夹加入python的搜索目录之下#####
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hq9a-xl%ki$-twjwwpcr)dlh)#ahjp*p&-rd%+ljafy$b5qfaw'

# SECURITY WARNING: don't run with debug turned on in production!
# 最后需要将settings的DEBUG改为FALSE，404时才会调用执行我们的404函数
# 要注意的是：当DEBUG为FALSE时，Django不会代管static和media的资源，
# 一般在生产环境下，静态资源会由第三方的服务器如Nginx来管理
DEBUG = True
######注意这里#####
ALLOWED_HOSTS = ['*']


# Application definition

######注意这里：注册app#####
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'fandom',
    'operation',
    'xadmin',
    'crispy_forms', #美化form页面
    'captcha',#验证码
    'pure_pagination',#分页
    'DjangoUeditor',#Ueditor
    'rest_framework'



]

#分页设置
PAGINATION_SETTINGS = {
'PAGE_RANGE_DISPLAYED': 3,#显示前三页数
'MARGIN_PAGES_DISPLAYED': 1,#显示后一页数
'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myFandom.urls'

######注意这里#####
AUTH_USER_MODEL="users.UserProfile"

#写入media，为了将{{ MEDIA_URL }}注册到html中
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        ######注意这里#####
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.core.context_processors.media',
                #"django.core.context_processors.request",  # 用于登陆重定向至登陆前页面,获取到request.path
            ],
        },
    },
]

WSGI_APPLICATION = 'myFandom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
######注意这里:配置数据库#####
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
         'NAME': "myfandom",
        'USER':"root",
        'PASSWORD':"mita",
        'HOST':"127.0.0.1",

        #'OPTIONS':{"init_command": "SET foreign_key_checks = 0;",},

    }
}

######注意这里#####修改默认的backend
AUTHENTICATION_BACKENDS=('users.views.CustomBackend',)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
######注意这里#####
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai' #时区

USE_I18N = True

USE_L10N = True

USE_TZ = False # 使用本地时间，而不是UTC时间，True为国际时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
######注意这里：配置静态文件路径#####
#当URL匹配到/static/时，则到STATICFILES_DIRS 下寻找
STATIC_URL = '/static/'
STATICFILES_DIRS=(os.path.join(BASE_DIR,"static"),)


#如果要让Django的服务器来代管静态资源，则需在settings中配置
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
#STATIC_ROOT=os.path.join(BASE_DIR,'static')

######注意：需要先开启邮箱的SMTP服务
EMAIL_HOST="smtp.163.com"
EMAIL_PORT=25
EMAIL_HOST_USER="13661025607@163.com"
EMAIL_HOST_PASSWORD="hcw15220182753"
EMAIL_USER_TLS=False
EMAIL_FROM="13661025607@163.com"




