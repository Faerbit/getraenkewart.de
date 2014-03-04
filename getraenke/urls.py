from django.conf.urls import patterns, url

from getraenke import views

urlpatterns = patterns('',
    url(r'^$', views.highscore, name="highscore"),
    url(r'^(?P<year>\d+)/$', views.highscore, name="highscore"),
    url(r'^manage/$', views.manage, name="manage"),
    url(r'^manage/(?P<year>\d+)/(?P<month>\d+)/$', views.manage, name="manage"),
    url(r'^people/$', views.people, name="people"),
)
