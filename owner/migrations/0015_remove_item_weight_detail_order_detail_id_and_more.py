# Generated by Django 5.1.2 on 2024-11-01 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0014_remove_item_weight_detail_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item_weight_detail',
            name='order_detail_id',
        ),
        migrations.AddField(
            model_name='item_weight_detail',
            name='order_detail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.order_detail'),
        ),
    ]
