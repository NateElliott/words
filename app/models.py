from django.contrib.auth.models import User
from django.db import models



class Projects(models.Model):

    name = models.TextField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Files(models.Model):

    name = models.TextField(max_length=255)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project_name')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class Paper(models.Model):

    name = models.TextField(max_length=255)
    store = models.TextField(max_length=255)
    is_public = models.BooleanField(default=True)
    origin = models.TextField(max_length=255)
    size = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
