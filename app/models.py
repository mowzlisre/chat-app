from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER = (('STUDENT','STUDENT'),('MENTOR','MENTOR'),('ADMIN','ADMIN'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=8, primary_key=True)
    user_type = models.CharField(max_length=55, choices=USER)
    mobile = models.CharField(max_length=10)
    is_complete = models.BooleanField()

    def __str__(self):
        return self.id

class Messages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id = models.CharField(max_length=8, primary_key=True)
    messages = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.id

class Class(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='member')
    texts = models.ManyToManyField(Messages)
    admin = models.ManyToManyField(User, related_name='admin')
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
