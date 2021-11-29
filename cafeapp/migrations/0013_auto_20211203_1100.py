# Generated by Django 3.2.9 on 2021-12-03 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0012_alter_order_order_time_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='../static/img/coffee.PNG', upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 3, 11, 0, 34, 421378)),
        ),
    ]