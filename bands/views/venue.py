# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from bands import helpers
from bands.models import Venue, Event


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

    for day in eventsbyday:
        day['events'].sort(helpers.order_latenight)

    return render(request, 'venue/detail.html', {
        'venue': venue,
        'events': eventsbyday,
    })