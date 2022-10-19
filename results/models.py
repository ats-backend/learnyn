import uuid

from django.db import models

# Create your models here.
from accounts.models import Student
from school.models import Subject


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, null=True)
    score = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.student.student_id


class Token(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.token
