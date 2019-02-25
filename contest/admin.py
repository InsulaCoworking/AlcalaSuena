# coding=utf-8
from django.contrib import admin

# Register your models here.
from bands.models import Band
from contest.models import BandMember, ContestBand, ContestJuryVote


def make_winner(self, request, queryset):

    bands_added = 0
    for band in queryset:
        band_exists = Band.objects.filter(name=band.name).count() > 0
        if band_exists:
            self.message_user(request, "'%s' ya se encontraba en el cartel definitivo." % band.name)
        else:
            new_band = Band.objects.create(
                name=band.name,
                city=band.city,
                genre=band.genre,
                tag=band.tag,
                profile_image=band.profile_image,
                band_image=band.band_image,
                num_members=band.num_members,
                description=band.description,
                embed_code=band.embed_code,
                embed_media=band.embed_media,
                instagram_link=band.instagram_link,
                facebook_link=band.facebook_link,
                youtube_link=band.youtube_link,
                twitter_link=band.twitter_link,
                bandcamp_link=band.bandcamp_link,
                presskit_link=band.presskit_link,
                webpage_link=band.webpage_link,
                spotify_link=band.spotify_link,
            )
            new_band.save()
            bands_added+=1

    if bands_added > 0:
        if bands_added == 1:
            message_bit = "Se ha añadido una nueva banda al cartel definitivo."
        else:
            message_bit = "Se añadieron %s nuevas bandas al cartel definitivo." % bands_added

        self.message_user(request, message_bit)

make_winner.short_description = "Añadir banda(s) al cartel definitivo"


class BandAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'city', 'num_members', 'has_local_member']
    ordering = ['name']
    actions = [make_winner]


admin.site.register(ContestBand, BandAdmin)
admin.site.register(BandMember)
admin.site.register(ContestJuryVote)
