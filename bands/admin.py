# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from bands.models import Band, Venue, Event

admin.site.register(Band)
admin.site.register(Venue)
admin.site.register(Event)