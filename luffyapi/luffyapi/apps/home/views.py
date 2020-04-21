from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
# 光标移动到要导报的类名或函数名或对象名或变量名，Alt+Enter 自动导包
from .models import Banner,Nav
from .serializers import BannerModelSerializer, NavModelSerializer
from luffyapi.settings import constants


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")[:constants.BANNER_LENGTH]
    serializer_class = BannerModelSerializer


class HeaderNavListAPIView(ListAPIView):
    '''头部导航'''
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=1).order_by('orders', '-id')[:constants.HEADER_NAV_LENGTH]
    serializer_class = NavModelSerializer


class FooterNavLIstAPIView(ListAPIView):
    '''脚部导航'''
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=2).order_by('orders','-id')[:constants.FOOTER_NAV_LENGTH]
    serializer_class = NavModelSerializer