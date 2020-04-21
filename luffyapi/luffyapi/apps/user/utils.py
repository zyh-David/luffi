from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django_redis import get_redis_connection

from luffyapi.settings import constants
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    redis_conn = get_redis_connection("cart")
    cart_num = redis_conn.hlen("cart_%s" % user.id)
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        "cart_num": cart_num,
        "credit": user.credit,
        "credit_money": constants.CREDIT_MONEY,
    }


def get_user_by_account(account):
    '''通过账号信息获取用户'''
    try:
        user = User.objects.get(Q(username=account) | Q(mobile=account))
    except User.DoesNotExist:
        user = None
    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)

      # 验证密码和是否允许登录
        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user