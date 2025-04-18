# Generated by Django 5.1.2 on 2024-10-31 02:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sunil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=1)),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
        migrations.CreateModel(
            name='office_employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
        migrations.CreateModel(
            name='Stock_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name_english', models.CharField(max_length=100)),
                ('item_name_marathi', models.CharField(max_length=100)),
                ('qty', models.IntegerField()),
                ('stock_qty', models.IntegerField(null=True)),
                ('weight', models.IntegerField()),
                ('stock_weight', models.IntegerField()),
                ('vehicle_number', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('stock_status', models.IntegerField(default=1)),
                ('party_name', models.CharField(max_length=200, null=True)),
                ('status', models.IntegerField(default=1)),
                ('purchase_amount', models.FloatField(default=0)),
                ('item_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.item_category')),
                ('office_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.office_employee')),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
    ]
