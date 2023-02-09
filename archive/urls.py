from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'archive'

urlpatterns = [
    url(r'^(?P<year>\d+)/$', views.archive_index, name='index'),
    url(r'^(?P<year>\d+)/bands/$', views.bands_list, name='bands_list'),
    url(r'^(?P<year>\d+)/bands/(?P<pk>\d+)/$', views.band_detail, name='band_detail'),
    url(r'^(?P<year>\d+)/contest/list/$', views.contest_entries_list, name='contest'),
    url(r'^(?P<year>\d+)/contest/bands/(?P<pk>\d+)/$', views.contest_band_detail, name='contest_band_detail'),
    url(r'^(?P<year>\d+)/timetable/$', views.timetable, name='timetables'),
]