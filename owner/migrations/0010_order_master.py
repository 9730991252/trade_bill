# Generated by Django 5.1.2 on 2024-11-01 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0009_alter_cart_qty'),
        ('sunil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hamali', models.FloatField()),
                ('tolai', models.FloatField()),
                ('aadat', models.FloatField()),
                ('shears', models.FloatField()),
                ('eater', models.FloatField()),
                ('total', models.FloatField()),
                ('order_filter', models.IntegerField(default=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('ordered_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.customer')),
                ('office_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='owner.office_employee')),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
    ]
