# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import TemplateView

from bands.forms.signup import SignUpForm
from bands.models import Event, Venue, Tag, Band
from core.mixins import SuperuserRequiredMixin


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
    tags = Tag.objects.current()

    lineup_first = Band.objects.current().filter(lineup_order=1)
    lineup_second = list(Band.objects.current().filter(lineup_order=2))
    lineup_third = list(Band.objects.current().filter(lineup_order=3))
    lineup_fourth = list(Band.objects.current().filter(lineup_order=4))

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


class SignUpView(CreateView):
    form_class = SignUpForm

    template_name = 'registration/register.html'

    def get_success_url(self):
        user = self.object
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()

        login(self.request, self.object)
        return reverse('contest_entries_list')


class ExportsDashboard(SuperuserRequiredMixin, TemplateView):
    template_name = 'export/index.html'
