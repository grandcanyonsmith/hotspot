from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.


class place_information(models.Model):
    place_image = models.ImageField(upload_to='photos')
    place_name = models.CharField(max_length=255)
    place_description = models.TextField()
    place_longitude = models.FloatField()
    place_latitude = models.FloatField()
    place_ratings = models.IntegerField()
    place_type = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    start_date_time = models.DateTimeField(null=True, blank=True)
    end_date_time = models.DateTimeField(null=True, blank=True)