from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from getraenkewart import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'getraenkewart.views.home', name='home'),
    # url(r'^getraenkewart/', include('getraenkewart.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^ente/', include(admin.site.urls)),
	url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^getraenke/', include('getraenke.urls')),
)
