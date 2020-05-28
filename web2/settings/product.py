#线上阶段的settings配置

DEBUG=False

import pymysql# 配置MySQL
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # 数据库引擎
        'NAME': 'web_db',         # 你要存储数据的库名，事先要创建
        'USER': 'root',         # 数据库用户名
        'PASSWORD': '1234',     # 密码
        'HOST': 'localhost',    # 主机
        'PORT': '3306',         # 数据库使用的端口
        # 'CONN_MAX_AGE':5*60,    #优化数据库连接
        # 'OPTIONS':{'charset':'utf8m64'}
    },
}
