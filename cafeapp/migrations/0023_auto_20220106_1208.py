# Generated by Django 3.2.9 on 2022-01-06 10:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0022_auto_20220104_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 6, 12, 8, 12, 720299)),
        ),
        migrations.AlterField(
            model_name='table',
            name='requested_on',
            field=models.DateField(default=datetime.date(2022, 1, 6)),
        ),
        migrations.AlterField(
            model_name='table',
            name='time_needed',
            field=models.TimeField(),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('paid_on', models.DateTimeField(default=datetime.datetime(2022, 1, 6, 12, 8, 12, 722414))),
                ('data', models.JSONField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafeapp.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
