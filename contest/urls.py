from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^bases/$', views.bases, name='bases'),
    url(r'^contest/signup/$', views.signup, name='contest_signup'),
    url(r'^contest/signup_success/$', views.form_success, name='form_success'),
    url(r'^contest/list/$', views.contest_entries_list, name='contest_entries_list'),
    url(r'^contest/bands/(?P<pk>\d+)$', views.contest_band_detail, name='contest_band_detail'),
    url(r'^contest/jury/$', views.contest_jury_list, name='contest_jury_list'),
    url(r'^contest/bands/(?P<pk>\d+)/vote/$', views.contest_band_vote, name='contest_band_vote'),
    url(r'^contest/jury/csv_votes/$', views.contest_csv_votes, name='contest_csv_votes'),
    url(r'^contest/jury/csv_bands/$', views.contest_csv_bands, name='contest_csv_bands'),

]