# Generated by Django 2.2.7 on 2019-11-24 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=500, verbose_name='广告标题')),
                ('image', models.ImageField(blank=True, null=True, upload_to='banner', verbose_name='广告图片')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='广告链接')),
                ('is_http', models.BooleanField(default=False, verbose_name='是否是站外链接')),
            ],
            options={
                'verbose_name': '广告轮播',
                'verbose_name_plural': '广告轮播',
                'db_table': 'ly_banner',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否显示')),
                ('orders', models.IntegerField(default=1, verbose_name='排序')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=500, verbose_name='导航标题')),
                ('link', models.CharField(max_length=500, verbose_name='导航链接')),
                ('position', models.IntegerField(choices=[(1, '头部导航'), (2, '脚部导航')], default=1, verbose_name='导航位置')),
                ('is_http', models.BooleanField(default=False, verbose_name='是否是站外地址')),
            ],
            options={
                'verbose_name': '导航菜单',
                'verbose_name_plural': '导航菜单',
                'db_table': 'ly_nav',
            },
        ),
    ]
