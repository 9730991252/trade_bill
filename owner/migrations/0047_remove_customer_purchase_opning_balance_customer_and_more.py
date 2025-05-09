# Generated by Django 5.1.2 on 2025-02-09 03:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0046_customer_purchase_opning_balance'),
        ('sunil', '0003_shope_contact_details_shope_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer_purchase_opning_balance',
            name='customer',
        ),
        migrations.AddField(
            model_name='customer_purchase_opning_balance',
            name='farmer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.farmer'),
        ),
        migrations.CreateModel(
            name='Customer_sell_opning_balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('type', models.IntegerField()),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.customer')),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
    ]
