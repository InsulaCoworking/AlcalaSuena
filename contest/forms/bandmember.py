from django import forms
from django.forms import formset_factory

from contest.models import BandMember


class BandMemberForm(forms.ModelForm):

    class Meta:
        model = BandMember
        exclude = ['band']
        widgets = {
            'image': forms.FileInput(attrs={}),
        }

    @staticmethod
    def getMembersFormset(band=None):
        extra_forms = 1 if (band is None or band.members.count() == 0) else 0
        return formset_factory(BandMemberForm, extra=extra_forms, can_delete=True )

    @staticmethod
    def save_members(band, formset):

        if band is None:
            return
        #print formset
        # Remove previous members to save new ones
        BandMember.objects.filter(band=band).delete()
        for member_form in formset:
            member = member_form.save(commit=False)
            member.band = band
            member.save()