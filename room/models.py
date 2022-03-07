from django.db import models

# Create your models here.
class rooms(models.Model):
    time=models.CharField(max_length=20)
    room=models.CharField(max_length=20)