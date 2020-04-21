from rest_framework import serializers

from .models import Banner, Nav


class BannerModelSerializer(serializers.ModelSerializer):
    """广告轮播的序列化器"""

    # 序列化器声明
    class Meta:
        model = Banner
        fields = ["image", "link", "is_http"]


class NavModelSerializer(serializers.ModelSerializer):
    """导航菜单的序列化器"""
    class Meta:
        model = Nav
        fields = ['title','link','is_http']