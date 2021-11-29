# Generated by Django 3.2.9 on 2021-12-02 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafeapp', '0007_alter_order_order_time_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='cart',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', related_query_name='fav_data', to='cafeapp.order'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]