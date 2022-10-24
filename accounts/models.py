from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from school.models import Classroom


# Create your models here.


class ResetPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=4, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)