# Generated by Django 2.2.7 on 2019-12-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20191210_2035'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoursePriceDiscout',
            new_name='CoursePriceDiscount',
        ),
        migrations.AlterModelOptions(
            name='coursediscount',
            options={'verbose_name': '价格优惠策略', 'verbose_name_plural': '价格优惠策略'},
        ),
        migrations.AlterField(
            model_name='coursediscount',
            name='discount_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursediscounts', to='course.CourseDiscountType', verbose_name='优惠类型'),
        ),
        migrations.AlterModelTable(
            name='coursediscount',
            table='ly_course_discount',
        ),
    ]
