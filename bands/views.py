# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from bands.models import Band


def index(request):
    bands = Band.objects.all()

    return render(request, 'index.html', { 'bands': bands })