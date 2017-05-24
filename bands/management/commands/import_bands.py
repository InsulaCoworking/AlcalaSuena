# coding: utf-8

"""
Management command to generate band token for easy editing
"""
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from bands.models import Band, BandToken, Tag


class Command(BaseCommand):
    help = "Generates new tokens for every band and lists them"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)



    def handle(self, *args, **options):

        tags = [
            '',
            'infantil',
            'clasica',
            'jazz_acustic',
            'rockpop',
            'worldmusic',
            'black',
            'electronica',
            'hiphop',
            'folk'
        ]

        csv_file = options['csv_file']
        ignorefirst = False
        with open(csv_file, 'rb') as f:

            reader = csv.reader(f, delimiter=';', quotechar='"')
            results = []
            for row in reader:
                if not ignorefirst:
                    ignorefirst = True
                    continue
                try:
                    tag = tags[int(row[4])]
                    style = Tag.objects.get(id=tag)
                except:
                    style = Tag.objects.get(id='unknown')

                band = Band()
                band.name = row[2]
                try:
                    band.num_members = int(row[3])
                except:
                    band.num_members = 0
                band.tag = style
                band.city = row[5]
                band.youtube_link = row[6]
                band.bandcamp_link = row[7]
                band.description = row[9]
                band.presskit_link = row[10]
                band.facebook_link = row[11]
                band.twitter_link = row[12]

                if band.facebook_link.startswith('facebook') or band.facebook_link.startswith('www'):
                    band.facebook_link = 'https://' + band.facebook_link
                #sanitize twitter
                if band.twitter_link.startswith('@'):
                    band.twitter_link = 'http://twitter.com/' + band.twitter_link[1:]

                if not band.bandcamp_link.startswith('http'):
                    band.bandcamp_link = None


                band.save()


import csv

