import uuid

from django.db import models

# Create your models here.
from accounts.models import Student
from school.models import Subject, Term, Session


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    exam_score = models.IntegerField(null=True, blank=True)
    first_assessment_score = models.IntegerField(null=True, blank=True)
    second_assessment_score = models.IntegerField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('student', 'subject')

    def __str__(self):
        return self.student.student_id

    def result_total(self):
        return self.first_assessment_score + self.second_assessment_score + self.exam_score


class Token(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.token
