from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    receiver = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)
    unread = models.BooleanField(null=True) 
    createdTime = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)


    fields = ['user', '_id', 'receiver', 'subject', 'message','unread']


    def __str__(self):
        return self.subject
