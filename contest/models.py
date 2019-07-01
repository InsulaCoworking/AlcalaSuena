# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Avg
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from archive.manager import ArchivedManager
from bands.helpers import RandomFileName
from bands.models import Tag


CRITERIA3_CHOICES = (
    (0, "Ninguna"),
    (2, "1"),
    (4, "2"),
    (6, "3"),
    (7, "Más de tres")
)





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
    instagram_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Instagram', max_length=250)

    is_validated = models.BooleanField(default=False, verbose_name='Criterios validados')
    validated_by = models.ForeignKey(User, null=True, blank=True, verbose_name='Validado por')

    criteria1 = models.BooleanField(default=False, verbose_name='¿El 50% de tus músicos o más tienen menos de 21 años?')
    criteria2 = models.BooleanField(default=False, verbose_name='¿Has realizado al menos 2 conciertos en los últimos 6 meses?')
    criteria2_extra = models.TextField(null=True, blank=True, verbose_name='Pega enlaces a alguna referencia web de los dos conciertos (evento en Fb, crónica, anuncio...)')
    criteria3 = models.IntegerField(default=0, verbose_name='¿Cuantas mujeres componen tu formación?', choices=CRITERIA3_CHOICES)

    criteria4 = models.BooleanField(default=False,
                                    verbose_name='¿Tienes algún álbum editado?')
    criteria4_extra = models.TextField(null=True, blank=True,
                                       verbose_name='Pega algún enlace donde poder esucharlo: Spotify, Bandcamp, etc')

    criteria5 = models.BooleanField(default=False, verbose_name='¿Tienes dossier de tu banda?')
    criteria6 = models.BooleanField(default=False, verbose_name='Tienes alguna crónica o crítica en algún medio?')
    criteria6_extra = models.TextField(null=True, blank=True, verbose_name='Pega enlaces a alguna referencia')

    criteria7 = models.BooleanField(default=False, verbose_name='¿Tienes redes sociales activas?')
    criteria8 = models.BooleanField(default=False, verbose_name='¿Al menos el 80% de tu repertorio son temas propios?')
    criteria9 = models.BooleanField(default=False, verbose_name='¿Tocaste o estabas programado el año pasado en Alcalá Suena?')

    archived = models.BooleanField(default=False, verbose_name='Archivada')
    archive_year = models.IntegerField(verbose_name='Año', null=True, blank=True)

    objects = ArchivedManager()

    class Meta:
        verbose_name = 'Banda concursante'
        verbose_name_plural = 'Bandas concursantes'
        ordering = ['name']

    @property
    def jury_points(self):
        points = ContestJuryVote.objects.filter(band=self).aggregate(sum=Avg('vote'))['sum']
        return int(points) if points else 0

    @property
    def total_points(self):

        return self.jury_points + self.criteria_points

    @property
    def criteria_points(self):
        points = 0

        if self.criteria1 == True:
            points += 7
        if self.criteria2 == True:
            points += 6
        points += self.criteria3 if self.criteria3 else 0
        if self.criteria4 == True:
            points += 10
        if self.criteria5 == True:
            points += 3
        if self.criteria6 == True:
            points += 3
        if self.criteria7 == True:
            rrss_points = 0
            rrss_points += 2 if self.instagram_link and self.instagram_link != '' else 0
            rrss_points += 2 if self.youtube_link and self.youtube_link != '' else 0
            rrss_points += 2 if self.bandcamp_link and self.bandcamp_link != '' else 0
            rrss_points += 2 if self.facebook_link and self.facebook_link != '' else 0
            rrss_points += 2 if self.twitter_link and self.twitter_link != '' else 0
            rrss_points += 2 if self.spotify_link and self.spotify_link != '' else 0
            rrss_points += 2 if self.webpage_link and self.webpage_link != '' else 0

            points += min(rrss_points, 6)
        if self.criteria8 == True:
            points += 8
        if self.criteria9 == True:
            points -= 25

        # As it can be negative...
        points = max(points, 0)
        return  points

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

    band = models.ForeignKey(ContestBand, verbose_name='Banda', related_name='jury_votes')
    voted_by = models.ForeignKey(User, verbose_name='Jurado', related_name='contest_votes')
    timestamp = models.DateTimeField(null=True, verbose_name='Timestamp')
    vote = models.IntegerField(default=0, verbose_name='Voto')

    class Meta:
        verbose_name = 'Voto del jurado'
        verbose_name_plural = 'Votos del jurado'
        ordering = ['band']
        unique_together = (("band", "voted_by"),)
        permissions = (("can_mange_jury", "Puede acceder al jurado"),)

    def __unicode__(self):
        return self.band.name + ': ' + self.voted_by.username + ': ' + str(self.vote)


class ContestPublicVote(models.Model):

    band = models.ForeignKey(ContestBand, verbose_name='Banda', related_name='public_votes')
    voted_by = models.ForeignKey(User, verbose_name='Votante', related_name='public_votes')
    timestamp = models.DateTimeField(null=True, verbose_name='Timestamp')

    class Meta:
        verbose_name = 'Voto del público'
        verbose_name_plural = 'Votos del público'
        ordering = ['band']
        unique_together = (("band", "timestamp"),)

    def __unicode__(self):
        return self.band.name + ': ' + self.voted_by.username + ': ' + str(self.timestamp)