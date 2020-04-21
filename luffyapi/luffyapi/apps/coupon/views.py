from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from datetime import datetime
from coupon.models import UserCoupon
from coupon.serializers import UserCouponModelSerializer


class UserCouponListAPIView(ListAPIView):

    queryset = UserCoupon.objects.filter( is_show=True, is_deleted=False, is_use = False )
    serializer_class = UserCouponModelSerializer
    # 使用过滤查哈获取当前用户有拥有的优惠券
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ('user_id',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user_id=request.user.id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)