from django.contrib.auth.models import User
from django.db import models


class Files(models.Model):

    name = models.TextField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

