# Generated by Django 5.1.2 on 2025-01-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0042_customer_purchase_payment_transaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_order_master',
            name='paid_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sell_order_master',
            name='paid_status',
            field=models.IntegerField(default=0),
        ),
    ]
