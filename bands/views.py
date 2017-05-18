# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from bands.models import Band, Venue, Event


def index(request):
    bands = Band.objects.all()

    return render(request, 'index.html', { 'bands': bands })

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