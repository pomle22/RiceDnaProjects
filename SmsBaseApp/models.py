from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='default')
    visit_num = models.PositiveIntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('SmsBaseApp:news_full_detail',args=[self.slug])

    class Meta:
        ordering = ['-created_on']
        

        def __str__(self):
            return self.title

       



class Contact(models.Model):
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    from_email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    message = models.TextField()


    
class Event(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   Start_event = models.DateTimeField(default=timezone.now)
   End_event = models.DateTimeField(default=timezone.now)
   image = models.ImageField(upload_to='event')


class About(models.Model):
    data = models.TextField(null=True)
    vision = models.TextField(null=True)
    mission = models.TextField(null=True)