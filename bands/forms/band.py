from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Band


class BandForm(forms.ModelForm):

    class Meta:
        model = Band
        fields = ['name', 'tag', 'genre', 'profile_image', 'band_image', 'city', 'num_members', 'description', 'embed_code']

