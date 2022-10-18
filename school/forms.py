from django import forms

from .models import Subject, Classroom


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name",)
        

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ( "is_active", "date_created" )