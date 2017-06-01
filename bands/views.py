# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# Create your views here.
from bands.forms.band import BandForm
from bands.models import Band, Venue, Event, BandToken, Tag

LATENIGHT_HOURS = datetime.time(5,0,0)

def order_latenight(event_a, event_b):
    print event_a.time
    print event_b.time
    if event_a.time == event_b.time:
        return 0
    elif event_a.time < LATENIGHT_HOURS:
        if event_b.time < LATENIGHT_HOURS:
            return 1 if event_a.time < event_b.time else -1
        else:
            return -1
    elif event_b.time < LATENIGHT_HOURS:
        return -1
    else:
        return 1 if event_a.time < event_b.time else -1

def index(request):
    share_filter = request.GET.get('share', None)
    if share_filter:
        try:
            events_list = map(lambda x: int(x), share_filter.split(','))
            events = Event.objects.filter(pk__in=events_list)
            return render(request, 'share.html', {'events':events})
        except ValueError:
            pass

    venues = Venue.objects.all()
    tags = Tag.objects.all()
    days = Event.objects.order_by('day').values_list('day', flat=True).distinct()

    return render(request, 'index.html', { 'venues': venues, 'tags':tags, 'days':days })

def venues_list(request):

    venues = Venue.objects.all()
    return render(request, 'venue/list.html', {'venues': venues})

def app_info(request):
    return render(request, 'app_info.html', {})

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

    for day in eventsbyday:
        day['events'].sort(order_latenight)

    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': eventsbyday,
    })

def bands_list(request):

    bands = list(Band.objects.all())
    tags = Tag.objects.all()
    random.shuffle(bands)
    return render(request, 'band/list.html', {
        'bands': bands, 'tags': tags
    })

def band_detail(request, pk):
    band = get_object_or_404(Band, pk=pk)
    events = Event.objects.filter(band=band)
    return render(request, 'band/detail.html', {
        'band': band,
        'events': events,
        'view': request.GET.get('view', None)
    })

def search(request):

    events = Event.objects.all()

    band_filter = request.GET.get('band', None)
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

        for eventsday in eventsbyday:
            if eventsday['day'] == event.day:
                day = eventsday
                break

        if day is None:
            day = { 'day': event.day, 'events':[] }
            eventsbyday.append(day)


        day['events'].append(event)

    for day in eventsbyday:
        day['events'].sort(order_latenight)

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