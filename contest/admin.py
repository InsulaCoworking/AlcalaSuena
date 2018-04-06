from django.contrib import admin

# Register your models here.
from contest.models import BandMember, ContestBand

admin.site.register(ContestBand)
admin.site.register(BandMember)