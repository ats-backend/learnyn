from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from school.models import Classroom
from students.models import Student


class StudentForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.active_objects.all(),
        widget=forms.Select(attrs={'class': "form-control form-control-lg"}),
        required=False
    )

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'email',
            'parent_firstname',
            'parent_lastname',
            'parent_email',
            'classroom'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with that email already exist"
            )
        return email

