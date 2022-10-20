from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from school.models import Classroom


# Create your models here.


class ActiveObject(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_suspended=False)


class Student(User):
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='students'
    )
    parent_firstname = models.CharField(max_length=40)
    parent_lastname = models.CharField(max_length=40)
    parent_email = models.EmailField(max_length=200)
    is_suspended = models.BooleanField(default=False)

    active_objects = ActiveObject()
    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(pre_save, sender=Student)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = instance.email.split('@')[0]
        instance.username = username


class ClassAdmin(User):
    classroom = models.OneToOneField(
        Classroom,
        on_delete=models.CASCADE,
        related_name='teacher',
        null=True
    )
    is_suspended = models.BooleanField(default=False)

    active_objects = ActiveObject()
    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(pre_save, sender=ClassAdmin)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = instance.email.split('@')[0]
        instance.username = username


class ResetPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=4, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
