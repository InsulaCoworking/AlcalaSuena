# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill
from bands.helpers import RandomFileName
from bands.models import Tag


class ContestBand(models.Model):
    name = models.CharField(null=False, verbose_name='Nombre de la banda/solista', max_length=240)
    tag = models.ForeignKey(Tag, related_name="contest_bands", verbose_name='Categoría del concurso')
    genre = models.CharField(null=True, blank=True, verbose_name='Género/Estilo', max_length=240)
    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('contest/'),
                                        processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG',
                                        verbose_name='Imagen principal')
    band_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('contest/'),
                                     processors=[ResizeToFit(1200, 600, upscale=False)], format='JPEG',
                                     verbose_name='Imagen de cabecera')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})
    city = models.CharField(null=True, blank=True, verbose_name='Ciudad de origen', max_length=140)
    num_members = models.IntegerField(null=True, blank=True, default=1, verbose_name='Número de miembros')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción/Biografía del grupo')
    comments = models.TextField(null=True, blank=True, verbose_name='Observaciones/Comentarios')

    embed_code = models.TextField(null=True, blank=True,
                                  verbose_name='Códido embed (enlace o iframe) para escucha (Bandcamp, Soundcloud, Spotify...)')
    embed_media = models.TextField(null=True, blank=True, verbose_name='Códido embed (enlace o iframe) de vídeo (Youtube, Vimeo...)')

    receiver_fullname = models.CharField(null=True, blank=True, verbose_name='Nombre de interesado', max_length=350)
    receiver_cif = models.CharField(null=True, blank=True, verbose_name='Documento (DNI/NIF/CIF)', max_length=30)

    has_local_member = models.BooleanField(default=False, verbose_name='Miembros locales')
    local_member_docs = models.FileField(null=True, blank=True, upload_to=RandomFileName('contest_docs/'), verbose_name='Documentación', max_length=180)

    rider_doc = models.FileField(null=False, blank=True, upload_to=RandomFileName('contest_docs/'),
                                         verbose_name='Rider técnico (adjuntar)', max_length=180)

    contact_email = models.CharField(null=False, blank=False, verbose_name='Email de contacto', max_length=250)
    contact_phone1 = models.CharField(null=False, blank=False, verbose_name='Teléfono de contacto', max_length=250)
    contact_phone2 = models.CharField(null=True, blank=True, verbose_name='Teléfono de contacto (2)', max_length=250)

    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    youtube_link = models.CharField(null=True, blank=True, verbose_name='Canal de Youtube', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    bandcamp_link = models.CharField(null=True, blank=True, verbose_name='Página de BandCamp', max_length=250)
    presskit_link = models.CharField(null=True, blank=True, verbose_name='Presskit', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    spotify_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Spotify', max_length=250)

    class Meta:
        verbose_name = 'Banda concursante'
        verbose_name_plural = 'Bandas concursantes'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class BandMember(models.Model):
    band = models.ForeignKey(ContestBand, verbose_name='Banda', related_name='Miembros')
    full_name = models.CharField(null=False, blank=False, verbose_name='Nombre y apellidos', max_length=350)
    dni = models.CharField(null=False, blank=False, verbose_name='Documento identidad', max_length=30)
    is_underage = models.BooleanField(default=False, verbose_name='Menor de edad')

    class Meta:
        verbose_name = 'Miembro de banda'
        verbose_name_plural = 'Miembros de bandas'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ': ' + self.full_name


class ContestJuryVote(models.Model):
    band = models.ForeignKey(ContestBand, primary_key=True, verbose_name='Banda', related_name='jury_votes')
    voted_by = models.ForeignKey(User, primary_key=True, verbose_name='Jurado', related_name='contest_votes')
    timestamp = models.DateTimeField(null=True, verbose_name='Timestamp')
    vote = models.IntegerField(default=0, verbose_name='Voto')

    class Meta:
        verbose_name = 'Voto del jurado'
        verbose_name_plural = 'Votos del jurado'
        ordering = ['band']

    def __unicode__(self):
        return self.band.name + ': ' + self.voted_by.username + ': ' + str(self.vote)
