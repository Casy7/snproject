# Generated by Django 2.2.6 on 2020-02-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreeFallApp', '0033_auto_20200205_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='text',
            field=models.CharField(blank=True, default='', max_length=2000, null=True),
        ),
    ]
