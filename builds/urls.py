from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<build_id>\d+)?$', views.router, name='index'),
    url(r'^favorite/(?P<build_id>\d+)$', views.favorite, name='favorite'),
    url(r'^browser$', views.browser, name='browser'),
]