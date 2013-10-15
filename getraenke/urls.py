from django.conf.urls import patterns, url

from getraenke import views

urlpatterns = patterns('',
    url(r'^$', views.highscore, name="highscore"),
    url(r'^(?P<year>\d+)/$', views.highscore, name="highscore"),
)
