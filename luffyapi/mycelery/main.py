# 主程序
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
import django
django.setup()
from celery import Celery
# 创建celery实例化对象
app = Celery('luffy')

# 通过app对象加载配置
app.config_from_object('mycelery.config')

# 自动搜索并加载任务
# 参数必须是一个了列表，里面的每一个任务都必须是任务的路径
# app.autodiscover_tasks([’任务‘，’任务‘])
app.autodiscover_tasks(["mycelery.mail","mycelery.sms"])

# 启动Celery的命令
# 强烈建议切换目录到项目目录下启动celery!!
# celery -A mycelery.main worker --loglevel=info
