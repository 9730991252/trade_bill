# Generated by Django 5.1.2 on 2025-01-22 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0027_order_master_discount'),
        ('sunil', '0003_shope_contact_details_shope_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marathi_name', models.CharField(max_length=100)),
                ('english_name', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=1)),
                ('shope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sunil.shope')),
            ],
        ),
    ]
