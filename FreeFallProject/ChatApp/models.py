from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
VISIBLE_FOR = [
    ("noone", "noone"),
    ("friends", "friends"),
    ("all", "all")]


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=250)
    visible_for = models.CharField(max_length=10,
                                   choices=VISIBLE_FOR, default="all")


class Profile(models.Model):
    avatar = models.ImageField(
        null=True, blank=True, upload_to='users/avatars/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=2000, blank=True)
    gender = models.CharField(max_length=20, default='male')
    see_hikes = models.CharField(
        max_length=10, choices=VISIBLE_FOR, default="all")
    add_to_participation = models.CharField(max_length=10,
                                            choices=VISIBLE_FOR, default="noone")
    request_for_participation = models.CharField(max_length=10,
                                                 choices=VISIBLE_FOR, default="all")


class Landmark(models.Model):
    def __str__(self):
        return f'{self.name}'
    name = models.CharField(max_length=200)
    image = models.ImageField(
        null=True, blank=True, upload_to='landmarks/')
    description = models.CharField(max_length=200000, default='desc')
    longitude = models.FloatField(default=0.0)
    is_public = models.BooleanField(default=True)
    latitude = models.FloatField(default=0.0)



class Hike(models.Model):
    creator = models.ForeignKey(
        User, null=True, default=None, related_name="creator", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='A new hike')
    description = models.CharField(max_length=200000, default='')
    short_description = models.CharField(max_length=1000, default='')

    participants = models.ManyToManyField(User, blank=True)

    landmarks = models.ManyToManyField(Landmark, blank=True)

    start_date = models.DateField(default="2020-01-02")
    end_date = models.DateField(default="2020-01-02")

    difficulty = models.CharField(max_length=200, default='none')
    type_of_hike = models.CharField(max_length=200, default='Пеший')

    coordinates = models.CharField(max_length=200000, default='[]')
    creation_datetime = models.DateTimeField(default=datetime.now())

    image = models.ImageField(null=True, blank=True, upload_to='hikes/')
