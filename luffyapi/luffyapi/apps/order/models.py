# Create your models here.
from django.db import models
from luffyapi.utils.models import BaseModel
from user.models import User
from course.models import Course
from ckeditor_uploader.fields import RichTextUploadingField


class Order(BaseModel):
    """订单模型"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices = (
        (1, '支付宝'),
        (2, '微信支付'),
    )
    order_title = models.CharField(max_length=150,verbose_name="订单标题")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="订单总价", default=0)
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="实付金额", default=0)
    order_number = models.CharField(max_length=64,verbose_name="订单号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    pay_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="支付方式")
    credit = models.IntegerField(default=0, null=True, verbose_name="使用的积分数量")
    coupon = models.IntegerField(default=0, null=True, verbose_name="用户优惠券ID")
    order_desc = RichTextUploadingField(verbose_name="订单描述")
    pay_time = models.DateTimeField(null=True, verbose_name="支付时间")
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING,verbose_name="下单用户")

    class Meta:
        db_table = "ly_order"
        verbose_name = "订单记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.order_title, self.total_price, self.real_price)


class OrderDetail(BaseModel):
    """订单详情"""
    order = models.ForeignKey(Order, related_name='order_courses', on_delete=models.CASCADE, verbose_name="订单")
    course = models.ForeignKey(Course, related_name='course_orders', on_delete=models.CASCADE, verbose_name="课程")
    expire = models.IntegerField(default='-1', verbose_name="有效期周期")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价")
    real_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程实价")
    discount_name = models.CharField(max_length=120, default="", verbose_name="优惠类型")

    class Meta:
        db_table = "ly_order_detail"
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.course.name)

    # 数据验证方法
    def validate(self, attrs):
        # todo credit
        # todo coupon
        return attrs

    # 模型的保存或者更新方法
    def create(self, validatrd_date):
        """保存订单"""
        pay_type = validatrd_date.get("pay_type")
        credit = validatrd_date.get('credit')
        coupon = validatrd_date.get('coupon')

        order_title = '路飞学城课程购买'
        toral_price = 0
        real_price = 0
        # 时间＋用户ＩＤ+随机数
        user_id = self.coutext['request'].user.id
        