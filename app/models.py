from django.contrib.auth.models import User
from django.db import models

from .helper import generator

# Create your models here.

class Paper(models.Model):

    name = models.TextField(max_length=255)
    store = models.TextField(max_length=255)
    is_public = models.BooleanField(default=True)
    origin = models.TextField(max_length=255)
    size = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name