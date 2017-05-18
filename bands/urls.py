from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^venues$', views.venues_list, name='venues_list'),
    url(r'^venues/(?P<pk>\d+)$', views.venue_detail, name='venue_detail'),
]