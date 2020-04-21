import logging
import random

from django.shortcuts import render

# Create your views here.
# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from luffyapi.libs.yuntongxun.sms import CCP
from luffyapi.settings import constants
from .utils import get_user_by_account
from .models import User
from .serializers import UserModelSerializer,UserSMSLoginModelSerializer
from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from rest_framework import status as http_status
from django.conf import settings
from mycelery.sms.tasks import send_sms


class GeetestCaptchaAPIView(APIView):
    """极验验证码视图类"""
    def __init__(self):
        super().__init__()

        self.gt = GeetestLib(settings.GEETEST["pc_geetest_id"], settings.GEETEST["pc_geetest_key"])
        self.user_id = "test"
        self.status = False

    def get(self,request):
        """获取验证码"""
        self.status = self.gt.pre_process(self.user_id)
        # 将来可以使用redis来保存status和user_id
        response_str = self.gt.get_response_str()
        return Response(response_str)

    def post(self,request):
        """验证码二次验证"""
        challenge = request.data.get(self.gt.FN_CHALLENGE, '')
        validate = request.data.get(self.gt.FN_VALIDATE, '')
        seccode = request.data.get(self.gt.FN_SECCODE, '')
        if self.status:
            result = self.gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = self.gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


class UserAPIView(CreateAPIView):
    """用户注册"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserSMSLoginAPIView(CreateAPIView):
    """用户短信登录"""
    queryset = User.objects.all()
    serializer_class = UserSMSLoginModelSerializer


"""
接口访问地址： /user/mobile/(?P<mobile>1[3-9]\d{9})/
"""
class MobileAPIView(APIView):
    def get(self,requset, mobile):
        """验证手机号码的唯一性"""
        # 1.根据手机号到数据库里面查找用户，返回结果
        try:
            User.objects.get(mobile=mobile)
            return Response({'status': False}, status=http_status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"status":True}, status=http_status.HTTP_200_OK)


"""
接口访问地址： /user/sms/(?P<mobile>1[3-9]\d{9})/
"""
log = logging.getLogger('django')


class SMSAPIView(APIView):
    def get(self, request, mobile):
        # from mycelery.mail.tasks import send_mail
        # send_mail.delay("649641514@qq.com")

        """短信发送"""
        redis_conn = get_redis_connection('sms_code')
        ret = redis_conn.get('mobile_%s' % mobile)
        if ret is not None:
            return Response({"message":'对不起，60秒内已经发送过短信，请耐心等待'},status=http_status.HTTP_400_BAD_REQUEST)

        # 2 .生成短信验证码
        sms_code = '%06d' % random.randint(1, 999999)

        # 3.保存短信验证码到redis
        # 开启事务【无法管理数据库的读取数据操作】
        pipe = redis_conn.pipeline()
        # redis_conn.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        # redis_conn.setex("mobile_%s" % mobile, constants.SMS_EXPIRE_TIME, '_')
        pipe.setex("mobile_%s" % mobile, constants.SMS_EXPIRE_TIME, '_')
        pipe.execute()
        # 4. 调用短信sdk, 发送短信
        # try:
            # ccp = CCP()
        print(mobile,sms_code,constants.SMS_EXPIRE_TIME // 60,constants.SMS_TEMPLATE_ID)

            # ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
            # print('ret:>', ret)
        send_sms.delay(mobile, sms_code)
            # ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
            # if ret == -1:
            #     log.error('用户注册短信发送失败！手机号：%s' % mobile)
            #     print(1)
            #     return Response({'message': '发送短信失败！'},status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except:
        #     print(2)
        #     return Response({'短信发送失败！'}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "发送短信成功！"})





