# Generated by Django 5.1.2 on 2024-10-30 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shope_name', models.CharField(max_length=100)),
                ('owner_name', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
