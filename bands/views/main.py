# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from bands import helpers
from bands.forms.newsForm import NewsForm
from bands.models import Event, Venue, Tag, Band


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

    lineup_first = Band.objects.filter(lineup_order=1)
    lineup_second = list(Band.objects.filter(lineup_order=2))
    lineup_third = list(Band.objects.filter(lineup_order=3))
    lineup_fourth = list(Band.objects.filter(lineup_order=4))

    days = Event.objects.order_by('day').values_list('day', flat=True).distinct()

    return render(request, 'index.html', {
        'venues': venues,
        'tags':tags,
        'days':days,
        'lineup_first': lineup_first,
        'lineup_second': lineup_second,
        'lineup_third': lineup_third,
        'lineup_fourth':lineup_fourth

    })



def lineup(request):

    lineup_first = Band.objects.filter(lineup_order=1)
    lineup_second = list(Band.objects.filter(lineup_order=2))
    lineup_third = list(Band.objects.filter(lineup_order=3))
    lineup_fourth = list(Band.objects.filter(lineup_order=4))

    days = Event.objects.order_by('day').values_list('day', flat=True).distinct()

    return render(request, 'lineup.html', {
        'days':days,
        'lineup_first': lineup_first,
        'lineup_second': lineup_second,
        'lineup_third': lineup_third,
        'lineup_fourth':lineup_fourth
    })


def app_info(request):
    return render(request, 'app_info.html', {})

def survey(request):
    return render(request, 'survey.html', {})

def search(request):

    events = Event.objects.all()
    band_filter = request.GET.get('band', None)
    venue_filter = request.GET.get('venue', None)
    tag_filter = request.GET.get('tag', None)
    day_filter = request.GET.get('day', None)

    if band_filter:
        events = events.filter(band__pk=band_filter)
    if venue_filter:
        events = events.filter(venue__pk=venue_filter)
    if tag_filter:
        events = events.filter(band__tag__pk=tag_filter)
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
            day = {'day': event.day, 'events': []}
            eventsbyday.append(day)

        day['events'].append(event)

    for day in eventsbyday:
        day['events'].sort(helpers.order_latenight)

    return render(request, 'search.html', {
                    'days': eventsbyday,
                    'num_days': len(eventsbyday),
                    'no_results': len(eventsbyday)==0
                  })

@csrf_exempt
def add_news(request):
    save_success = False
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            api_key = request.POST.get('api_key', None)
            if api_key == settings.APP_APIKEY:
                form.save()
                save_success = True
                return HttpResponse()
            else:
                return HttpResponseBadRequest()
    else:
        form = NewsForm()

    if save_success:
        form = NewsForm()

    return render(request, 'add_news.html', {
        'save_success':save_success,
        'form': form,
    })
