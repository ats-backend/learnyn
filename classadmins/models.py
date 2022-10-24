from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from school.models import Classroom


# Create your models here.


class ActiveObject(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_suspended=False)


class ClassAdmin(User):
    classroom = models.OneToOneField(
        Classroom,
        on_delete=models.CASCADE,
        related_name='teacher',
        null=True
    )
    is_suspended = models.BooleanField(default=False)

    active_objects = ActiveObject()
    objects = UserManager()

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(pre_save, sender=ClassAdmin)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = instance.email.split('@')[0]
        instance.username = username

