from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from school.models import Classroom

from .models import ClassAdmin, Student


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "A user with that email already exist"
            )
        return email

    def clean_username(self):
        email = self.cleaned_data.get('email')
        username = email.split('@')[0]
        return username


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email:
            raise ValidationError(
                "Email is required"
            )

        if not password:
            raise ValidationError(
                "Password is required"
            )
        username = email.split('@')[0]
        if not authenticate(username=username, password=password):
            raise ValidationError(
                "Invalid email or password, please try again"
            )
        return self.cleaned_data


class ClassAdminForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.active_objects.all(),
        widget=forms.Select(attrs={'class': "form-control form-control-lg"})
    )

    class Meta:
        model = ClassAdmin
        fields = (
            'first_name',
            'last_name',
            'email',
            'classroom'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "A user with that email already exist"
            )
        return email


class PasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise ValidationError(
                "The passwords must match"
            )
        return self.cleaned_data


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
            raise ValidationError(
                "A user with that email already exist"
            )
        return email
