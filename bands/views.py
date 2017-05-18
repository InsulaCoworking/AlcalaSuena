# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from bands.models import Band, Venue, Event


def index(request):
    bands = Band.objects.all()
    venues = Venue.objects.all()

    return render(request, 'index.html', { 'bands': bands, 'venues': venues })

def venues_list(request):

    venues = Venue.objects.all()
    return render(request, 'venue/list.html', {'venues': venues})

def venue_detail(request, pk):

    venue = get_object_or_404(Venue, pk=pk)
    events = Event.objects.filter(venue=venue)
    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': events,
    })

def band_detail(request, pk):

    band = get_object_or_404(Band, pk=pk)
    events = Event.objects.filter(band=band)
    return render(request, 'band/detail.html', {
        'band': band,
        'events': events,
    })

def search(request):

    events = Event.objects.all()

    band_filter = request.GET.get('band', None)
    print band_filter
    if band_filter:
        events = events.filter(band__pk=band_filter)

    venue_filter = request.GET.get('venue', None)
    if venue_filter:
        events = events.filter(venue__pk=venue_filter)

    return render(request, 'search.html', {
                      'events': events,
                  })