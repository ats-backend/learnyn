from django.contrib.auth.models import User
from django.db import models

from school.models import Classroom
# Create your models here.


class Student(User):
    student_id = models.CharField(max_length=10, unique=True)
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='students'
    )
    parent_firstname = models.CharField(max_length=40)
    parent_lastname = models.CharField(max_length=40)
    parent_email = models.EmailField(max_length=200)


class ClassAdmin(User):
    classroom = models.OneToOneField(
        Classroom,
        on_delete=models.CASCADE,
        related_name='teacher'
    )

