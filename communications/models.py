from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
import pytz

# Create your models here.

TZ_CHOICES = ((tz, tz) for tz in pytz.all_timezones)

class Store(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)
    timezone = models.CharField(max_length=50, null=False, blank=False, choices=TZ_CHOICES) 
    phone_number = models.CharField(max_length=12, null=False, blank=False)


class Discount(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=10, null=False, blank=False)


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    operator_group = models.CharField(max_length=20) ## NEED TO ASK ABOUT THIS AND PROBABLY CHANGE


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, null=False, blank=True, choices=TZ_CHOICES) 
    phone_number = models.CharField(max_length=12, null=False, blank=False)


class Conversation(models.Model):
    ## conversation status choices
    CHOICES = (("P", "PENDING"), ("R", "RESOLVED"))

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, null=False, blank=False, choices=CHOICES, default="P") 

class Chat(models.Model):
    ## chat status choices
    CHOICES = (("N", "NEW"), ("S", "SENT"))

    conversation = models.ForeignKey(Conversation, related_name='chats', on_delete=models.CASCADE)
    payload = models.TextField(blank=False, null=False)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)  ## NEED DATETIME FIELD
    status = models.CharField(max_length=20, null=False, blank=False, choices=CHOICES, default="N") 


class Schedule(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sending_date = models.DateTimeField()

