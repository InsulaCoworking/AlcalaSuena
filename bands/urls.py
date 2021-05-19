from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^app/$', views.app_info, name='app_info'),
    url(r'^lineup/$', views.lineup, name='lineup'),
    url(r'^survey/', views.survey, name='survey'),
    url(r'^venues/$', views.venues_list, name='venues_list'),
    url(r'^venues/(?P<pk>\d+)$', views.venue_detail, name='venue_detail'),

    url(r'^bands/$', views.bands_list, name='bands_list'),
    url(r'^bands/(?P<pk>\d+)$', views.band_detail, name='band_detail'),
    url(r'^band/edit/(?P<token>\w+)$', views.edit_band, name='edit_band'),
    url(r'^bands/csv_bands/$', views.csv_bands, name='csv_bands'),

    url(r'^event/(?P<pk>\d+)/$', views.EventDetail.as_view(), name='event_detail'),

    url(r'^horarios/$', views.all_venues_timetable, name='timetable'),
    url(r'^timetable/$', views.timetable2, name='timetables'),
    url(r'^news/add/$', views.add_news, name='add_news'),

    url(r'^billing/$', views.billing_form, name='billing'),
    url(r'^billing/list/$', views.billing_list, name='billing'),
    url(r'^billing/download/$', views.download_csv, name='download_csv'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]