from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class change_contents(models.Model):
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField()
    image_contents = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class new_event(models.Model):
    title = models.CharField(max_length=255, blank=True)
    detail = models.TextField()
    image_evevt = models.CharField(max_length=255)
    image_gallery = models.TextField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title




class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


