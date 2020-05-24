from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
VISIBLE_FOR = [
    ("noone", "noone"),
    ("friends", "friends"),
    ("all", "all")]

TYPE_OF_NOTIFICATION = [
    ("request_for_ptc", "request_for_ptc"),
    ("invite_to_hike", "invite_to_hike"),
    ("user_added_to_hike", "user_added_to_hike"),
    ("simple_text", "simple_text")
]

MEMBER_JOIN = [
    ("open","open"),
    ("request","request"),
    ("close","close"),
]


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
    limit_of_members = models.IntegerField(default=15, blank=True)

    landmarks = models.ManyToManyField(Landmark, blank=True)

    start_date = models.DateField(default="2020-01-02")
    end_date = models.DateField(default="2020-01-02")

    join_to_group = models.CharField(max_length=10, default='request', choices=MEMBER_JOIN)
    difficulty = models.CharField(max_length=200, default='none')
    type_of_hike = models.CharField(max_length=200, default='Пеший')

    coordinates = models.CharField(max_length=200000, default='[]')
    creation_datetime = models.DateTimeField(auto_now=True)

    image = models.ImageField(null=True, blank=True, upload_to='hikes/')


class Post(models.Model):
    post_author = models.ForeignKey(User, null=True, default=None, related_name="post_author", on_delete=models.CASCADE)
    hike = models.ForeignKey(
        Hike, default='', null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=20000, default='')
    creation_datetime = models.DateTimeField(auto_now=True) 


class Message(models.Model):
    def __str__(self):
        return f'{self.name}'
    name = models.CharField(max_length=200, default='')
    author = models.ForeignKey(User, null=True, default=None, related_name="author", on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=200000, default='')
    hike = models.ForeignKey(
        Hike, default='', null=True, on_delete=models.CASCADE)


class Day(models.Model):
    def __str__(self):
        return f'{self.name}'
    hike = models.ForeignKey(
        Hike, default='', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to='days/')
    caption = models.CharField(max_length=200, default='', blank=True)
    description = models.CharField(max_length=200000, default='')
    date = models.DateField(default="2020-01-02")
    coordinates = models.CharField(max_length=200000, default='[]')


class Notification(models.Model):

    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)
    type_of_notification = models.CharField(
        max_length=25, choices=TYPE_OF_NOTIFICATION, default="simple_text")
    from_user = models.ForeignKey(User, related_name='from_user', blank=True, null=True, default='', on_delete=models.CASCADE)
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE, default='', blank=True)
    text = models.CharField(max_length=2000, default='', blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)

