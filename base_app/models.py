from django.db import models

# Create your models here.

class Measurements(models.Model):
    search_type = models.CharField(max_length=100)
    text_sample = models.TextField(max_length=500)
    text_length = models.IntegerField()
    result = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
