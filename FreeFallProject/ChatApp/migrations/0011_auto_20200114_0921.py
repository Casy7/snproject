# Generated by Django 3.0 on 2020-01-14 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0010_auto_20200114_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hike',
            name='creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 14, 9, 21, 1, 515579)),
        ),
    ]