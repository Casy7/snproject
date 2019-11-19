from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StandartUser (User):
    # username = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, default='male')


class Hike(models.Model):
    name = models.CharField(max_length=200, default='A new hike')
    description = models.CharField(max_length=200000, default='desc')
    start_date = models.DateField(default="2020-01-02")
    end_date = models.DateField(default="2020-01-02")
    image = models.ImageField(null=True)
    creator = models.ForeignKey(User, null = True, default=None, related_name="creator", on_delete = models.CASCADE)
    # members = models.ManyToManyField(StandartUser, limit_choices_to=200)