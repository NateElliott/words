from django.contrib.auth.models import User
from django.db import models


class Files(models.Model):

    name = models.TextField(max_length=255)
    store = models.TextField(max_length=128)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    chash = models.TextField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

