from django.db import models
# Create your models here.
from user.models import User
from luffyapi.utils.models import BaseModel


class Coupon(BaseModel):
    """优惠券"""
    coupon_choices = (
        (0, '折扣优惠'),
        (1, '减免优惠')
    )
    name = models.CharField(max_length=32, verbose_name='优惠卷标题')
    coupon_type = models.SmallIntegerField(choices=coupon_choices, default=0, verbose_name="优惠券类型")
    timer = models.IntegerField(verbose_name='优惠卷有效期', default=30, help_text='')
    condition = models.IntegerField(blank=True, default=0, verbose_name='使用优惠券的价格条件')
    sale = models.TextField(verbose_name='优惠公式', help_text="""
        *号开头表示折扣价，例如*0.82表示八二折；<br>
        -号开头表示减免价,例如-10表示在总价基础上减免10元<br>    
        """)

    class Meta:
        db_table = "ly_coupon"
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.name)


class UserCoupon(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coupons", verbose_name="用户")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="users", verbose_name="优惠券")
    start_time = models.DateTimeField(verbose_name="优惠券有效期的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠券有效期的结束时间")
    is_use = models.BooleanField(default=False, verbose_name='优惠券是否使用')

    class Meta:
        db_table = "ly_user_coupon"
        verbose_name = '用户的优惠券'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "优惠券：%s,用户：%s" % (self.coupon.name, self.user.username)
