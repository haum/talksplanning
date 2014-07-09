from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('talksplanning.views',
    url(r'^/?$', 'home', name='home'),
    url(r'^b/(?P<id>\d+)/?$', 'batch_detail', name='batch_detail'),
    url(r'^b/(?P<batch_id>\d+)/inscription$', 'batch_form', name='batch_form'),
    url(r'^b/(?P<batch_id>\d+)/proposal$', 'talk_form', name='talk_form'),
)

