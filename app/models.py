from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.crypto import get_random_string

class Profile(models.Model):
    USER = (('STUDENT','STUDENT'),('MENTOR','MENTOR'),('ADMIN','ADMIN'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=8, primary_key=True, default=get_random_string(8).lower())
    user_type = models.CharField(max_length=55, choices=USER)
    mobile = models.CharField(max_length=10)
    is_complete = models.BooleanField()

    def __str__(self):
        return self.id

class Messages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    messages = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.id

class Class(models.Model):
    PRIV = (('OPEN', 'OPEN'), ('INVITE ONLY', 'INVITE ONLY'), ('CLOSED', 'CLOSED'))
    TEXT = (('ALL', 'ALL'), ('ADMINS ONLY', 'ADMINS ONLY'))
    id = models.CharField(max_length=8, primary_key=True, default=get_random_string(8).lower())
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='member')
    texts = models.ManyToManyField(Messages, blank=True)
    admin = models.ManyToManyField(User, related_name='admin')
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    privacy = models.CharField(max_length=15, choices=PRIV, default='OPEN')
    texting = models.CharField(max_length=15, choices=TEXT, default='ALL')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name


class Invite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviter+')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitee+')
    code = models.CharField(max_length=8, primary_key=True, default=get_random_string(8).lower())
    clss = models.ForeignKey(Class, on_delete=models.CASCADE)
    invalid = models.BooleanField()

    def __str__(self):
        return self.code
    