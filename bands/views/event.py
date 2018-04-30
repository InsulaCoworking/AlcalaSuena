from django.http import HttpResponse
from django.shortcuts import render

from bands.models import Event


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
    print events_byday

    eventdays = []
    for day in events_byday:
        events = Event.objects.filter(day=day).order_by('time')

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


    print eventdays
    return render(request, 'timetable.html', {
                    'days': eventdays,
                    'num_days': len(eventdays),
                  })