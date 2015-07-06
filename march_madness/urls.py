from django.conf.urls import patterns, url

from march_madness import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
