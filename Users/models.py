from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="images/", default='media/photos/image.jpg')
    attachment = models.FileField(upload_to="attachments", default='media/storage/image.jpg')
    location = models.TextField(max_length=300, blank=True) 
    tel = models.CharField(max_length=15, blank=True) 
    birth_date = models.DateField(null=True, blank=True)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE) 
    last_login = models.DateTimeField(null = True, blank=True)






    



