from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from .models import User
from rest_framework_jwt.settings import api_settings

import re


class UserModelSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    sms = serializers.CharField(write_only=True, max_length=6, min_length=4, help_text='短信验证码')
    token = serializers.CharField(max_length=1024, read_only=True, min_length=1, help_text="token认证字符串")

    class Meta:
        model = User
        fields = ["id", "username", "token", "password", "mobile", "sms", "credit"]
        # 字段的额外申明
        extra_kwargs = {
            'id': {'read_only': True, },
            'username': {'read_only': True, },
            'password': {'write_only': True, 'min_length': 6, },
            'mobile': {'write_only': True, 'min_length': 11}
        }

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms')

        password = attrs.get('password')
        print("sms_code",sms_code, "mobile", mobile,"password",password)
        # 验证手机号码的格式
        ret = re.match(r'1[3-9]\d{9}$', mobile)
        if not ret:
            raise serializers.ValidationError('对不起，手机号格式错误！')
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError('对不起，手机号已经被注册')
        except User.DoesNotExist:
            pass

        # 验证短信是否正确
        redis_conn = get_redis_connection('sms_code')
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        print(real_sms_code, sms_code)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('对不起，短信验证码错误！本次验证码已失效，请重新发送！')
        # 本次验证以后，直接删除当前本次验证码，防止出现恶意破解
        redis_conn.delete("sms_%s" % mobile)
        return attrs

    def create(self, validated_data):
        """用户信息"""
        # 移除不需要的数据
        print(validated_data.pop('sms'))
        # mobile = validated_data.get('mobile')
        # password = validated_data.get('password')
        # username=mobile
        # try:
        #     user = User.objects.create_user(username=username, password=password, mobile=mobile)
        # except:
        #     raise serializers.ValidationError("创建用户失败！")
        raw_password = validated_data.get('password')
        hash_password = make_password(raw_password)
        # 对用户设置一个默认值
        username = validated_data.get('mobile')
        # 调用序列化器提供的create方法
        user = User.objects.create(
            mobile=username,
            username=username,
            password=hash_password,
        )
        # 使用restframework_jwt模块提供手动生成token的方法生成登录状态

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user


class UserSMSLoginModelSerializer(serializers.ModelSerializer):
    """用户登录序列化器"""
    sms = serializers.CharField(write_only=True, max_length=6, min_length=4, help_text='短信验证码')
    token = serializers.CharField(max_length=1024, read_only=True, min_length=1, help_text="token认证字符串")


    class Meta:
        model = User
        fields = ["id", "token", "mobile", "sms"]
        # 字段的额外申明
        extra_kwargs = {
            'id': {'read_only': True, },
            'username': {'read_only': True, },
            'password': {'write_only': True, 'min_length': 6, },
            'mobile': {'write_only': True, 'min_length': 11}
        }

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms')

        print("sms_code",sms_code, "mobile", mobile)
        # 验证手机号码的格式
        ret = re.match(r'1[3-9]\d{9}$', mobile)
        if not ret:
            raise serializers.ValidationError('对不起，手机号格式错误！')

        user = User.objects.get(mobile=mobile)


        # 验证短信是否正确
        redis_conn = get_redis_connection('sms_code')
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        print(real_sms_code, sms_code)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('对不起，短信验证码错误！本次验证码已失效，请重新发送！')
        # 本次验证以后，直接删除当前本次验证码，防止出现恶意破解
        redis_conn.delete("sms_%s" % mobile)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        print('序列化器return')
        return attrs


