# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from contest.models import ContestBand


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class BandForm(BaseForm):

    rider_doc = forms.FileField(required=True, label='Rider técnico (adjuntar)')
    read_terms = forms.BooleanField(required=True, initial=False, label='He leído y acepto las bases del concurso')

    class Meta:
        model = ContestBand
        exclude=[]
        widgets= {
            'name': forms.TextInput(attrs={'class': 'linked-value', 'data-ref':'#band-name'}),
            'genre': forms.TextInput(attrs={'class': 'linked-value', 'data-ref': '#band-genre'}),
        }

