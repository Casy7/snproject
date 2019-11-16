from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StandartUser (User):
    # username = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, default='male')


class Hike(models.Model):
    name = models.CharField(max_length=200, default='A new hike')
    description = models.CharField(max_length=200000, default='desc')
    user = models.ForeignKey(StandartUser, on_delete = models.CASCADE)