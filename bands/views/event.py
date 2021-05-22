from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from bands import helpers
from bands.models import Event, Venue, Tag


def event_detail(request, pk):

    event = get_object_or_404(Event, pk=pk)
    return redirect('event_detail_slug', pk=pk, slug=event.slug)


class EventDetail(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'event/detail.html'



class EventPoster(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'event/poster_card.html'


def timetable(request):
    if not request.user.has_perm('contest.can_mange_jury'):
        return HttpResponse('Unauthorized', status=401)
    '''
        if band_filter:
        events = events.filter(band__pk=band_filter)
    if venue_filter:
        events = events.filter(venue__pk=venue_filter)
    if tag_filter:
        events = events.filter(band__tag__pk=tag_filter)
    if day_filter:
        events = events.filter(day=day_filter)

    :param request:
    :return:
    '''

    events_byday = Event.objects.dates('day', 'day')
    eventdays = []
    for day in events_byday:
        events = Event.objects.filter(day=day).order_by('-venue', 'time')

        venues = []
        for event in events:
            venue = None
            for eventsvenue in venues:
                if eventsvenue['venue'] == event.venue:
                    venue = eventsvenue
                    break

            if venue is None:
                venue = {'venue': event.venue, 'events': []}
                venues.append(venue)

            venue['events'].append(event)

        eventdays.append({'day':day, 'venues':venues})

    return render(request, 'timetable.html', {
                    'days': eventdays,
                    'num_days': len(eventdays),
                  })



def timetable2(request):

    events_byday = Event.objects.dates('day', 'day')
    venues = Venue.objects.all().order_by('-name')
    tags = Tag.objects.current()
    days = []
    for day in events_byday:
        daydate = {
            'day': day,
            'venues': venues,
            'events':  list(Event.objects.filter(day=day).order_by('time'))
        }
        daydate['events'].sort(helpers.order_latenight)


        days.append(daydate)


    return render(request, 'timetable2.html', {
                    'days': days,
                    'tags':tags,
                    'venues':venues,
                    'num_days': len(days),
                  })