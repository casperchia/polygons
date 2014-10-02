from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degrees/$', 'degree_list'),
    url(r'^degree/(?P<program_id>\d+)/$', 'program_details'),
    url(r'^planner/$', 'create_plan'),
)
