from django.contrib import admin

# Register your models here.
from contest.models import BandMember, ContestBand, ContestJuryVote

admin.site.register(ContestBand)
admin.site.register(BandMember)
admin.site.register(ContestJuryVote)