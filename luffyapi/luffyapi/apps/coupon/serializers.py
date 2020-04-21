from rest_framework import serializers

from coupon.models import Coupon, UserCoupon


class CouponModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('name', 'coupon_type', 'condition', 'sale')


class UserCouponModelSerializer(serializers.ModelSerializer):
    coupon = CouponModelSerializer()

    class Meta:
        model = UserCoupon
        fields = ("id", "start_time", "end_time", "coupon")
