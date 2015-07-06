from django.conf.urls import patterns, url

from umpire import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

