# Generated by Django 3.0 on 2020-01-14 07:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreeFallApp', '0008_auto_20200114_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hike',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 9, 17, 9, 317386)),
        ),
    ]
