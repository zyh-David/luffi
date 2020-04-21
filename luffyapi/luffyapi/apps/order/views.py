from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from .models import Order
from .serializers import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    """生成订单"""
    serializer_class = OrderModelSerializer
    queryset = Order.objects.filter(is_show=True, is_deleted=False)