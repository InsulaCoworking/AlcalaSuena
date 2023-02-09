# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from archive.admin import ArchiveFilter
from bands.models import Band, Venue, Event, Tag, BandToken, Settings
from bands.models.billing_info import BillingInfo
from bands.models.news import News

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(BandToken)
admin.site.register(Settings)
admin.site.register(News)
admin.site.register(BillingInfo)




class BandAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'city', 'archive_year']
    ordering = ['name']
    actions = ['archive']
    list_filter = (ArchiveFilter,)

    def archive(self, request, queryset):
        # All requests here will actually be of type POST
        # so we will need to check for our special key 'apply'
        # rather than the actual request type

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


admin.site.register(Band, BandAdmin)