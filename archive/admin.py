# coding=utf-8
from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bands.models import Band
from contest.models import BandMember, ContestBand, ContestJuryVote


class ArchiveFilter(SimpleListFilter):
  title = 'Archivada' # a label for our filter
  parameter_name = 'archive' # you can put anything here

  def lookups(self, request, model_admin):
    # This is where you create filter options; we have two:
    return [
        ('archived', 'Archivadas'),
        ('not_archived', 'No archivadas'),
    ]

  def queryset(self, request, queryset):
    # This is where you process parameters selected by use via filter options:
    if self.value() == 'archived':
        # Get websites that have at least one page.
      return queryset.distinct().filter(archived=True)

    if self.value():
        # Get websites that don't have any pages.
        return queryset.distinct().filter(archived=False)


class BandAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'city', 'num_members', 'has_local_member']
    ordering = ['name']
    actions = ['make_winner', 'archive']
    list_filter = (ArchiveFilter,)

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
                bands_added += 1

        if bands_added > 0:
            if bands_added == 1:
                message_bit = "Se ha añadido una nueva banda al cartel definitivo."
            else:
                message_bit = "Se añadieron %s nuevas bandas al cartel definitivo." % bands_added

            self.message_user(request, message_bit)

    make_winner.short_description = "Añadir banda(s) al cartel definitivo"

    def archive(self, request, queryset):
        # All requests here will actually be of type POST
        # so we will need to check for our special key 'apply'
        # rather than the actual request type
        print queryset

        if 'apply' in request.POST:
            # The user clicked submit on the intermediate form.

            year = request.POST['year']
            # Perform our update action:
            queryset.update(archived=True, archive_year=year)

            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            self.message_user(request,
                              "Archivadas {} bandas".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'contest/archive_admin.html',
                      context={'bands': queryset})

    archive.short_description = "Archivar"


admin.site.register(ContestBand, BandAdmin)
admin.site.register(BandMember)
admin.site.register(ContestJuryVote)
