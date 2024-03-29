"""alcalasuena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from api.urls import get_api

from bands import urls as bands_urls
from contest import urls as contest_urls
from archive import urls as archive_urls
from core import urls as core_urls

urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^', include(bands_urls)),
    url(r'^', include(contest_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^archive/', include(archive_urls, namespace='archive')),
    url(r'^api/', include(get_api('v1').urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
