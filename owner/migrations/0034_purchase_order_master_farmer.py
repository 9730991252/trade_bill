# Generated by Django 5.1.2 on 2025-01-26 04:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0033_purchase_order_detail_purchase_order_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order_master',
            name='farmer',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.farmer'),
        ),
    ]
