# Generated by Django 2.2.6 on 2019-11-25 16:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0012_auto_20191125_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hike',
            name='participants',
            field=models.ManyToManyField(blank=True, limit_choices_to=200, to=settings.AUTH_USER_MODEL),
        ),
    ]