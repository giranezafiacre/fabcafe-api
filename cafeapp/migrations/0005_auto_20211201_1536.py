# Generated by Django 3.2.9 on 2021-12-01 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0004_order_ordered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_timedate',
            new_name='order_time_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]