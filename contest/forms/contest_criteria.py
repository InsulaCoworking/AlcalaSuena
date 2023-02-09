# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.forms import Textarea

from contest.models import ContestBand


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, Textarea):
                field.widget.attrs['rows'] = 3

            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class ContestCriteriaForm(BaseForm):

    class Meta:
        model = ContestBand
        fields= ('is_validated', 'criteria1', 'criteria2', 'criteria2_extra', 'criteria3', 'criteria4', 'criteria4_extra', 'criteria5', 'criteria6', 'criteria6_extra', 'criteria7', 'criteria8', 'criteria9')

