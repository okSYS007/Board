from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    user_status = models.BooleanField(default = False)