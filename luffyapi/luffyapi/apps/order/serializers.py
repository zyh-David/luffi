from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers

from coupon.models import UserCoupon
from course.models import Course
from luffyapi.settings import constants
from .models import Order, OrderDetail


class OrderModelSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    # 模型
    class Meta:
        model = Order
        fields = ["order_number", "total_price", "real_price", "pay_type", "credit", "coupon"]
        read_only_fields = ["order_number", "total_price", "real_price"]
        extra_kwargs = {
            "pay_type": {"write_only": True, "default": 1},
            "credit": {"write_only": True, "min_value": 0},
            "coupon": {"write_only": True},
        }

    # 数据验证方法
    def validate(self, attrs):
        # 判断积分是否在合理的使用范围内
        user = self.context['request'].user
        credit = attrs.get('credit')
        coupon = attrs.get('coupon')
        if credit > 0:
            if credit >user.credit:
                raise serializers.ValidationError('对不起，您当前的积分不足！')
            # 判断优惠券是否已经使用或者在可使用时间范围内
            now_time = datetime.now()
            try:
                if coupon != 0:
                    UserCoupon.objects.filter(coupon=coupon, is_show=True, is_deleted=False, is_use=False,start_time__lte=now_time, end_time__gt=now_time)
            except UserCoupon.DoesNotExist:
                raise serializers.ValidationError('对不起，无法使用当前优惠券！')
        return attrs

    # 模型的保存或者更新方法
    def create(self, validated_data):
        """保存订单"""
        pay_type = validated_data.get('pay_type')
        credit = validated_data.get('credit')
        coupon = validated_data.get('coupon')

        order_title = '路飞学城课程购买'
        total_price = 0
        real_price = 0
        # 时间＋用户＋随机数
        from datetime import datetime
        import random
        user_id = self.context['request'].user.id

        order_number = datetime.now().strftime("%Y%m%d%H%M%S")+('%06d' % user_id)+("%05d" % random.randint(0,99999))
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                order = Order.objects.create(
                    order_title=order_title,
                    total_price=total_price,
                    real_price=real_price,
                    order_number=order_number,
                    order_status=0,
                    pay_type=pay_type,
                    # credit=credit,
                    # coupon=coupon,
                    user_id=user_id
                )
                redis_conn = get_redis_connection('cart')

                # 记录当前订单定义的课程信息到订单详情

                cart_hash = redis_conn.hgetall('cart_%s' % user_id)
                selected_set = redis_conn.smembers('selected_%s' % user_id)
                pipe = redis_conn.pipeline()
                pipe.multi()
                for course_id_bytes in selected_set:
                    course_id = course_id_bytes.decode()
                    aa= cart_hash.get(course_id_bytes)
                    expire_time = int( cart_hash.get(course_id_bytes).decode())
                    course = Course.objects.get(pk=course_id)
                    order_detail = OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_time,
                        price=course.real_price(expire_time),
                        real_price=course.real_price(expire_time),
                        # discount_name='原价购买',
                    )
                    # 从购物车中删除对应的商品课程
                    pipe.hdel('cart_%s' % user_id, course_id)
                    pipe.srem('selected _%s' % user_id, course_id)
                    total_price += float(order_detail.price)
                    # 计算订单的总价格
                # 判断是否使用了积分，如果使用了积分，则积分抵扣金额
                if credit >0 :
                    # 判断是否使用了优惠券，如果使用了优惠券，抵扣优惠券的优惠金额
                    credit_price = credit / constants.CREDIT_MONEY
                if coupon > 0:
                    user = self.context['request'].user
                    coupon = validated_data.get('coupon')
                    now_time = datetime.now()
                    try:
                        result = UserCoupon.objects.get(pk=coupon, is_deleted=False, is_show=True, user_id=user.id, start_time__lt=now_time, end_time__gt=now_time)
                    except UserCoupon.DoesNotExist:
                        raise serializers.ValidationError('对不起，当前的优惠不存在或者已过期不可用！')
                    sale = result.coupon.sale
                    if result.coupon.coupon_type == 0:
                        # 折扣优惠
                        coupon_price = total_price * (1-float(sale[1:]))
                    else:
                        # 减免优惠
                        coupon_price = float(sale[1:])

                # 提交redis事务操作
                pipe.execute()

                # 填写总价格和优惠后的价格
                order.total_price = total_price
                order.real_price = total_price - credit/constants.CREDIT_MONEY - coupon_price

            except:
                transaction.savepoint_rollback(save_id)
                return serializers.ValidationError("订单生成失败！")

        return order
