# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# Create your views here.
from bands.forms.band import BandForm
from bands.models import Band, Venue, Event, BandToken, Tag

LATENIGHT_HOURS = datetime.time(3,0,0)

def index(request):
    bands = Band.objects.all()
    venues = Venue.objects.all()
    tags = Tag.objects.all()
    days = Event.objects.order_by('day').values_list('day', flat=True).distinct()

    print days
    return render(request, 'index.html', { 'bands': bands, 'venues': venues, 'tags':tags, 'days':days })

def venues_list(request):

    venues = Venue.objects.all()
    return render(request, 'venue/list.html', {'venues': venues})

def venue_detail(request, pk):

    venue = get_object_or_404(Venue, pk=pk)
    events = Event.objects.filter(venue=venue)

    eventsbyday = []
    for event in events:
        day = None
        for eventsday in eventsbyday:
            if eventsday['day'] == event.day:
                day = eventsday
                break

        if day is None:
            day = {'day': event.day, 'events': []}
            eventsbyday.append(day)
        day['events'].append(event)

    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': eventsbyday,
    })

def bands_list(request):

    bands = Band.objects.all()
    tags = Tag.objects.all()
    return render(request, 'band/list.html', {
        'bands': bands, 'tags': tags
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

    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        events = events.filter(band__tag__pk=tag_filter)

    day_filter= request.GET.get('day', None)
    if day_filter:
        events = events.filter(day=day_filter)

    eventsbyday = []
    for event in events:
        day = None

        #we reduce the day to the previous one
        if event.time < LATENIGHT_HOURS:
            event.day = event.day - datetime.timedelta(days=1)

        for eventsday in eventsbyday:
            if eventsday['day'] == event.day:
                day = eventsday
                break

        if day is None:
            day = { 'day': event.day, 'events':[] }
            eventsbyday.append(day)


        day['events'].append(event)

    return render(request, 'search.html', {
                      'days': eventsbyday,
                      'num_days': len(eventsbyday),
                        'no_results':len(eventsbyday)==0
                  })


def edit_band(request, token):
    token = BandToken.objects.filter(token=token)
    if not token or not token[0].band or (token[0].expiration_date and token[0].expiration_date >= timezone.now()):
        return render(request, 'band/badtoken.html', {'token': token})

    band = token[0].band
    save_success = False
    if request.method == "POST":
        form = BandForm(request.POST, request.FILES, instance=band)
        print form.is_valid()
        if form.is_valid():
            band = form.save()
            print band.band_image
            save_success = True
    else:
        form = BandForm(instance=band)
    return render(request, 'band/edit.html', {'band':band, 'form': form, 'save_success': save_success })