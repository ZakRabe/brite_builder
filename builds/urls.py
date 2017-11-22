from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.router, name='index'),
    url(r'^favorite/(?P<build_id>\d+)$', views.favorite, name='favorite'),
]