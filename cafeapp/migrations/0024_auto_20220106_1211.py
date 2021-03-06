# Generated by Django 3.2.9 on 2022-01-06 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0023_auto_20220106_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 6, 12, 11, 2, 470387)),
        ),
        migrations.AlterField(
            model_name='table',
            name='time_needed',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='paid_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 6, 12, 11, 2, 472532)),
        ),
    ]
