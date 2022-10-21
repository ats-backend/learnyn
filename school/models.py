import datetime

from django.db import models
from django.core.exceptions import ValidationError


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


first = f"{(datetime.datetime.today() - datetime.timedelta(days=365)).year}/{datetime.datetime.today().year}"
second = f"{datetime.datetime.today().year}/{(datetime.datetime.today() + datetime.timedelta(days=365)).year}"


class Session(models.Model):
    SESSION_CHOICES = (
        (first, first),
        (second, second)
    )
    name_of_session = models.CharField(max_length=32, null=True, choices=SESSION_CHOICES, unique=True)

    def __str__(self):
        return self.name_of_session


class Term(models.Model):
    TERM_CHOICES = (
        ("First Term", "First Term"),
        ("Second Term", "Second Term"),
        ("Third Term", "Third Term")
    )
    session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE)
    term = models.CharField(choices=TERM_CHOICES, max_length=32, null=True)

    def __str__(self):
        return self.term

    class Meta:
        unique_together = ("session", "term")


class Subject(models.Model):
    name = models.CharField(max_length=50, null=True, )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if Subject.active_objects.filter(name=self.name).first():
    #         raise ValidationError("Subject already exist")
    #     return super(Subject, self).save(*args, **kwargs)


class Classroom(models.Model):
    CATEGORY_CHOICES = (
        ("Primary", "Primary"),
        ("Secondary(Junior)", "Secondary(Junior)"),
        ("Secondary(Senior)", "Secondary(Senior)"),
    )
    name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY_CHOICES)
    subjects = models.ManyToManyField(Subject, limit_choices_to={'is_active': True}, )
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if Classroom.active_objects.filter(name=self.name, category=self.category).first():
    #         raise ValidationError("Classroom already exist")
    #     return super(Classroom, self).save(*args, **kwargs)

    @property
    def number_of_students(self):
        return self.students.count()

    @property
    def class_admin(self):
        return self.teacher

    @property
    def number_of_subjects_offerred(self):
        return self.subjects.all().count()
