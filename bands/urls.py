from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^app$', views.app_info, name='app_info'),
    url(r'^survey', views.survey, name='survey'),
    url(r'^venues$', views.venues_list, name='venues_list'),
    url(r'^venues/(?P<pk>\d+)$', views.venue_detail, name='venue_detail'),

    url(r'^bands$', views.bands_list, name='bands_list'),
    url(r'^bands/(?P<pk>\d+)$', views.band_detail, name='band_detail'),
    url(r'^bands/(?P<pk>\d+)$', views.band_detail, name='band_detail'),
    url(r'^band/edit/(?P<token>\w+)$', views.edit_band, name='edit_band'),
    url(r'^billing', views.billing, name='billing'),
]