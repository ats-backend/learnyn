from django import forms

from results.models import Token, Result
from school.models import Subject


class StudentResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['subject', 'score']
        widgets = {
            'subject': forms.Select(attrs={'class': "form-control form-control-lg",
                                           'required': True}),
            'score': forms.TextInput(attrs={'class': "form-control form-control-lg",
                                            'required': True})
        }


ResultFormset = forms.formset_factory(ResultForm, extra=9)


class TokenForm(forms.Form):
    token = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                                          'required': True}))
