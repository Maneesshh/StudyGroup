from django.db import models

from django.contrib.auth.models import AbstractUser

from .constants import Status



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) :
        return self.name
    

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) :
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) :
        return self.body[0:50]

class Media(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    media_name = models.CharField(max_length=255, null=True)
    media_type = models.CharField(max_length=100, null=True)
    media_size = models.IntegerField(null=True)
    media_path = models.FileField(upload_to='files/',null=True)

    def __str__(self):
        return self.media_name
    

class VideoStatus(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    host = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50,default=Status.INACTIVE)
    ended = models.DateTimeField(null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status

