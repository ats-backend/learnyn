from django.db import models

from accounts.models import Teacher

# Create your models here.
class ActiveManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    
class InActiveManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)



class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


class Classroom(models.Model):
    name = models.CharField(max_length=50, null=True)
    subjects = models.ManyToManyField(Subject)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()
    