from django.db import models
from luffyapi.utils.models import BaseModel


# Create your models here.
class Banner(BaseModel):
    """轮播图模型"""
    # 字段
    title = models.CharField(max_length=500, verbose_name='广告标题')
    # upload_to 表示设置保存文件的子目录,系统会自动创建
    image = models.ImageField(upload_to="banner", null=True, blank=True, verbose_name="广告图片")
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name="广告链接")
    is_http = models.BooleanField(default=False, verbose_name="是否是站外链接")

    # 表信息
    class Meta:
        db_table = "ly_banner"
        verbose_name = "广告轮播"
        verbose_name_plural = verbose_name

    # 自定义方法和自定义字段
    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航菜单"""
    NAV_OPTION = (
        (1, '头部导航'),
        (2, '脚部导航'),
    )
    title = models.CharField(max_length=500, verbose_name='导航标题')
    link = models.CharField(max_length=500, verbose_name='导航链接')
    position = models.IntegerField(choices=NAV_OPTION, default=1, verbose_name="导航位置")
    is_http = models.BooleanField(default=False, verbose_name='是否是站外地址')

    class Meta:
        db_table ='ly_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name

    # 自定义方法[自定义字段或者自定义工具方法]
    def __str__(self):
        return self.title

