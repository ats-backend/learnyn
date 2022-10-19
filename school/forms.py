from tkinter import Widget
from django import forms

from .models import Subject, Classroom


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            })
        }


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ("is_active", "date_created")
        widgets = {
            "name": forms.TextInput(attrs={
                'class': "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control"
            }),

            # "subjects": forms.ChoiceWidget(attrs={
            #     "class": "form-control"
            # }),
        }
