#开发阶段的 settings 配置
from .base import * #NOQA      #这个注释的作用是：告诉PEP8规范检测工具，这个地方不需要检测

DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'pympler'
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',  # 注意检查中间件先后顺序
    ]
    INTERNAL_IPS = ("127.0.0.1",)
    DEBUG_TOOLBAR_CONFIG = {
        "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',  # 304
    }
    DEBUG_TOOLBAR_PANELS=[
        'pympler.panels.MemoryPanel',
    ]