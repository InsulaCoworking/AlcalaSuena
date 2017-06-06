from django import forms

from bands.models.billing_info import BillingInfo


class BillingForm(forms.ModelForm):

    class Meta:
        model = BillingInfo
        exclude=[]
