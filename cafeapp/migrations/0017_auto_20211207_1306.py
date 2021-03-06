# Generated by Django 3.2.9 on 2021-12-07 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0016_auto_20211207_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('1', 'coffee'), ('2', 'softdrinks'), ('3', 'snacks')], max_length=25),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 7, 13, 6, 33, 825195)),
        ),
    ]
