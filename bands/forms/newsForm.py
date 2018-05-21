from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Band
from bands.models.news import News
from contest.forms.band import BaseForm


class NewsForm(BaseForm):

    api_key = forms.CharField(max_length=100, widget=forms.HiddenInput, required=False)

    class Meta:
        model = News
        exclude=[]

