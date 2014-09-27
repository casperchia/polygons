from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degree_planner/program_details/(?P<program_id>\d+)/$','program_details'),
)
