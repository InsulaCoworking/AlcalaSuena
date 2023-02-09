from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    url(r'^bases/$', views.bases, name='bases'),
    url(r'^concurso/$', views.contest_index, name='contest_index'),
    url(r'^contest/signup/$', views.signup, name='contest_signup'),
    url(r'^contest/$', views.contest_dashboard, name='contest_dashboard'),
    url(r'^contest/signup_success/$', views.form_success, name='form_success'),
    url(r'^contest/list/$', views.contest_entries_list, name='contest_entries_list'),
    url(r'^contest/bands/(?P<pk>\d+)$', views.contest_band_detail, name='contest_band_detail'),
    url(r'^contest/bands/(?P<pk>\d+)/delete$', views.DeleteContestBand.as_view(), name='contest_band_delete'),
    url(r'^contest/jury/$', views.contest_jury_list, name='contest_jury_list'),
    url(r'^contest/jury/bands/(?P<pk>\d+)/vote/$', views.contest_band_vote, name='contest_band_vote'),
    url(r'^contest/jury/csv_votes/$', views.contest_csv_votes, name='contest_csv_votes'),
    url(r'^contest/jury/csv_bands/$', views.contest_csv_bands, name='contest_csv_bands'),
    url(r'^contest/jury/csv_user_votes/$', views.contest_csv_user_votes, name='contest_csv_user_votes'),
    url(r'^contest/jury/csv_receiver_info/$', views.contest_receiver_info, name='contest_receiver_info'),
    url(r'^contest/jury/csv_participants_info/$', views.contest_participants_info, name='contest_participants_info'),
    url(r'^contest/jury/csv_riders/$', views.contest_rider_info, name='contest_riders_info'),

    url(r'^contest/privacy_policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^privacidad/$', views.PrivacyPolicies.as_view(), name='privacy'),

    url(r'^contest/login/$', views.social_login, name='contest_social_login'),
    url(r'^contest/bands/(?P<pk>\d+)/vote/$', views.contest_public_vote, name='contest_public_vote'),
    url(r'^contest/my_vote/$', views.contest_user_votes, name='contest_user_votes'),

]