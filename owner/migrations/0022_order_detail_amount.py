# Generated by Django 5.1.2 on 2024-11-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0021_phonepe_transition'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
