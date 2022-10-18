from django.db import models


# Create your models here.
from accounts.models import Student


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # subject = models.OneToOneField('Subject', on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, max_digits=4)
