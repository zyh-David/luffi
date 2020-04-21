import xadmin
from .models import Credit
class CreditModelAdmin(object):
    """订单详情模型管理类"""
    list_display = ["id","user","opera","number"]
xadmin.site.register(Credit, CreditModelAdmin)