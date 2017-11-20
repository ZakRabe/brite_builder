"""brite_builder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views
from talents import urls as talent_urls
from builds import urls as build_urls
from site_auth import urls as auth_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/?$', views.profile, name='profile'),
    url(r'^talents/', include(talent_urls)),
    url(r'^builds/', include(build_urls)),
    url(r'^auth/', include(auth_urls)),
    url(r'^(?P<champ_name>\w+-*\w*)?/(?P<loadout>.*)/(?P<build_id>\d+)?$', views.build, name='build'),
    url(r'^(?P<champ_name>\w+-*\w*)?/?$', views.index, name='index'),
]

