# Generated by Django 2.2.6 on 2020-01-18 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreeFallApp', '0015_auto_20200118_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='landmark',
            name='latitude',
            field=models.CharField(default='0.0', max_length=200),
        ),
        migrations.AddField(
            model_name='landmark',
            name='longitude',
            field=models.CharField(default='0.0', max_length=200),
        ),
        migrations.AlterField(
            model_name='hike',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 18, 17, 10, 36, 269047)),
        ),
    ]
