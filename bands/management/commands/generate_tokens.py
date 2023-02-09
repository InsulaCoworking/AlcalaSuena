# coding: utf-8

"""
Management command to generate band token for easy editing
"""
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from bands.models import Band, BandToken


class Command(BaseCommand):
    help = "Generates new tokens for every band and lists them"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        bands = Band.objects.all()
        for band in bands:
            BandToken.objects.filter(band=band).delete()
            token = get_random_string(length=12)
            new_token = BandToken.objects.create(band=band, token=token)
