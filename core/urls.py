from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.SignUpView.as_view(), name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True }, name='login'),
    url(r'^logout/$',  auth_views.LogoutView.as_view(), name='logout'),
    url(r'^exports/$', views.ExportsDashboard.as_view(), name='exports_dashboard'),
]