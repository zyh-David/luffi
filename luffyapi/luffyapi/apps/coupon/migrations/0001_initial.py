# Generated by Django 2.2.7 on 2019-12-15 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, verbose_name='优惠卷标题')),
                ('coupon_type', models.SmallIntegerField(choices=[(0, '折扣优惠'), (1, '减免优惠')], default=0, verbose_name='优惠券类型')),
                ('timer', models.IntegerField(default=30, verbose_name='优惠卷有效期')),
                ('condition', models.IntegerField(blank=True, default=0, verbose_name='使用优惠券的价格条件')),
                ('sale', models.TextField(help_text='\n        *号开头表示折扣价，例如*0.82表示八二折；<br>\n        -号开头表示减免价,例如-10表示在总价基础上减免10元<br>    \n        ', verbose_name='优惠公式')),
            ],
            options={
                'verbose_name': '优惠券',
                'verbose_name_plural': '优惠券',
                'db_table': 'ly_coupon',
            },
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('start_time', models.DateTimeField(verbose_name='优惠券有效期的开始时间')),
                ('end_time', models.DateTimeField(verbose_name='优惠券有效期的结束时间')),
                ('is_use', models.BooleanField(default=False, verbose_name='优惠券是否使用')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='coupon.Coupon', verbose_name='优惠券')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户的优惠券',
                'verbose_name_plural': '用户的优惠券',
                'db_table': 'ly_user_coupon',
            },
        ),
    ]
