from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from school.models import Classroom

# Create your models here.


class ActiveObject(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(
            is_suspended=False,
            is_deleted=False
        )


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
    is_deleted = models.BooleanField(default=False)

    active_objects = ActiveObject()
    objects = UserManager()

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def student_class(self):
        return self.classroom.name


@receiver(pre_save, sender=Student)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = instance.email.split('@')[0]
        instance.username = username


@receiver(post_save, sender=Student)
def set_student_id(sender, instance, created, **kwargs):
    if created:
        id2string = str(instance.id).zfill(4)
        student_id = f"LYN-STD-{id2string}"
        instance.student_id = student_id
        instance.save()

