from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# the classroom model is meant to be in the school app which has not been created
# the only way to make migrations with for Student and Teacher models is to have their
# related model created. So the Classroom model is only tentative till it exists in the school app


class Classroom(models.Model):
    pass


class Student(User):
    student_id = models.CharField(max_length=10, unique=True)
    classroom = models.ForeignKey(
        'Classroom',
        on_delete=models.CASCADE,
        related_name='students'
    )
    parent_firstname = models.CharField(max_length=40)
    parent_lastname = models.CharField(max_length=40)
    parent_email = models.EmailField(max_length=200)


class ClassAdmin(User):
    classroom = models.OneToOneField(
        'Classroom',
        on_delete=models.CASCADE,
        related_name='teacher'
    )

