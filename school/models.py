from django.db import models


from accounts.models import Student, ClassAdmin


# Create your models here.
class ActiveManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    
class InActiveManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)



class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()
    
    
    def __str__(self):
        return self.name


class Classroom(models.Model):
    CATEGORY_CHOICES = (
        ("Primary", "Primary"),
        ("Secondary(Junior)", "Secondary(Junior)"),
        ("Secondary(Senior)", "Secondary(Senior)"),
    )
    name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY_CHOICES)
    subjects = models.ManyToManyField(Subject)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()
    
    def __str__(self):
        return self.name
    
    
    @property
    def number_of_students(self):
        return Student.objects.filter(classroom_id=self.id).count()
    
    @property
    def students(self):
        return Student.objects.filter(classroom_id=self.id)
    
    @property
    def class_admin(self):
        return ClassAdmin.objects.get(classroom_id=self.id)
    
    @property
    def number_of_subjects_offerred(self):
        return self.subjects.all().count()
    