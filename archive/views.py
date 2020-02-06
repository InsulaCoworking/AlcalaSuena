# coding=utf-8
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from bands import helpers
from bands.helpers import get_query
from bands.models import Tag, Band, Event, Venue
from contest.forms.contest_criteria import ContestCriteriaForm
from contest.models import ContestBand, ContestJuryVote


def contest_entries_list(request, year):

    bands = ContestBand.objects.archived(year)
    band_count = bands.count()
    tag_filter = request.GET.get('tag', None)
    if tag_filter:
        bands = bands.filter(tag__pk=tag_filter)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['name', 'genre', 'city'])
        if entry_query:
            bands = bands.filter(entry_query)

    paginator = Paginator(bands, 9)
    page = request.GET.get('page')
    try:
        bands = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bands = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        bands = paginator.page(paginator.num_pages)

    params = {
        'ajax_url': reverse('archive:contest', kwargs={'year':year}),
        'year':year,
        'query_string': query_string,
        'band_count': band_count,
        'bands': bands,
        'page': page
    }
    print params['ajax_url']

    if request.is_ajax():
        response = render(request, 'archive/contest_search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['tags'] = Tag.objects.all()
        return render(request, 'archive/contest_list.html', params)


def contest_band_detail(request, year, pk):
    band = get_object_or_404(ContestBand, pk=pk)

    view_data = {
        'band': band,
        'view': request.GET.get('view', None),
        'year': year,
    }

    return render(request, 'archive/band_detail.html', view_data )


def bands_list(request, year):

    bands = list(Band.objects.archived(year))
    tags = Tag.objects.all()
    random.shuffle(bands)
    return render(request, 'archive/band_list.html', {
        'bands': bands, 'tags': tags, 'year':year
    })

def band_detail(request, year, pk):
    band = get_object_or_404(Band, pk=pk)
    events = Event.objects.filter(band=band)
    return render(request, 'archive/band_detail.html', {
        'band': band,
        'year':year,
        'events': events,
        'view': request.GET.get('view', None)
    })


def timetable(request, year):

    events_byday = Event.objects.filter(band__archived=True, band__archive_year=year).dates('day', 'day')
    venues = Venue.objects.all().order_by('-name')
    tags = Tag.objects.all()
    days = []
    print events_byday
    for day in events_byday:
        print day
        daydate = {
            'day': day,
            'venues': venues,
            'events':  list(Event.objects.filter(day=day).order_by('time'))
        }
        daydate['events'].sort(helpers.order_latenight)
        days.append(daydate)

    return render(request, 'archive/timetable.html', {
                    'days': days,
                    'tags':tags,
                    'venues':venues,
                    'year':year,
                    'num_days': len(days),
                  })


def archive_index(request, year):

    venues = Venue.objects.all()
    tags = Tag.objects.all()

    lineup_first = Band.objects.archived(year).filter(lineup_order=1)
    lineup_second = list(Band.objects.archived(year).filter(lineup_order=2))
    lineup_third = list(Band.objects.archived(year).filter(lineup_order=3))
    lineup_fourth = list(Band.objects.archived(year).filter(lineup_order=4))

    days = Event.objects.order_by('day').values_list('day', flat=True).distinct()

    return render(request, 'archive/index.html', {
        'venues': venues,
        'year':year,
        'tags':tags,
        'days':days,
        'lineup_first': lineup_first,
        'lineup_second': lineup_second,
        'lineup_third': lineup_third,
        'lineup_fourth':lineup_fourth

    })

