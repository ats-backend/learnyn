from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet

from accounts.models import ClassAdmin
from results.models import Token, Result
from school.models import Subject


class StudentResultForm(forms.ModelForm):
    TERM_CHOICES = (
        ("First Term", "First Term"),
        ("Second Term", "Second Term"),
        ("Third Term", "Third Term")
    )

    r_term = forms.ChoiceField(choices=TERM_CHOICES)

    class Meta:
        model = Result
        fields = ['student', 'r_term', 'session']


class ResultForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super(ResultForm, self).__init__(*args, **kwargs)
    #     teacher = ClassAdmin.objects.filter(id=user.id).first()
    #     self.fields['subject'].queryset = Subject.objects.filter(classroom__teacher=user)

    class Meta:
        model = Result
        fields = ['subject', 'first_assessment_score', 'second_assessment_score', 'exam_score']
        widgets = {
            'subject': forms.Select(attrs={'class': "form-control form-control-lg",
                                           'required': True}),
            'first_assessment_score': forms.TextInput(attrs={'class': "form-control form-control-lg",
                                                             'required': True}),
            'second_assessment_score': forms.TextInput(attrs={'class': "form-control form-control-lg",
                                                              'required': True}),
            'exam_score': forms.TextInput(attrs={'class': "form-control form-control-lg",
                                                 'required': True})
        }


class BaseSubjectFormset(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        subjects = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            subject = form.cleaned_data.get('subject')
            if subject in subjects:
                raise ValidationError("Results must have distinct subject name")
            subjects.append(subject)


ResultFormset = forms.formset_factory(ResultForm, formset=BaseSubjectFormset, extra=9)


class TokenForm(forms.Form):
    token = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                                          'required': True}))
