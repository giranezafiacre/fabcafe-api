# Generated by Django 3.2.9 on 2021-12-01 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0006_auto_20211201_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time_date',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]
