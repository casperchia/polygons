from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degree_planner/$','degree_planner'),
    url(r'^degree_planner/program/(?P<program_id>\d+)/$','program'),
)
