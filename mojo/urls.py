from django.conf.urls import patterns, url

from mojo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
