from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Description(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length=20, default='male')


class Landmark(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200000, default='desc')
    
    def __str__(self):
        return f'{self.name}'  

class Hike(models.Model):
    name = models.CharField(max_length=200, default='A new hike')
    description = models.CharField(max_length=200000, default='desc')
    participants = models.ManyToManyField(User, blank=True)
    landmarks = models.ManyToManyField(Landmark)
    start_date = models.DateField(default="2020-01-02")
    end_date = models.DateField(default="2020-01-02")
    difficulty = models.CharField(max_length=200, default='none')
    type_of_hike = models.CharField(max_length=200, default='Пеший')
    image = models.ImageField(null=True)
    coordinates = models.CharField(max_length=200000, default='')
    creator = models.ForeignKey(User, null=True, default=None, related_name="creator", on_delete=models.CASCADE)


