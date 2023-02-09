from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Band


class BandForm(forms.ModelForm):

    class Meta:
        model = Band
        exclude=[]

