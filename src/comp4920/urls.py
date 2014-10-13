from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degrees/$', 'degree_list'),
    url(r'^degree/(?P<program_id>\d+)/$', 'program_details'),
    url(r'^degree/plan/(?P<program_plan_id>\d+)/$', 'program_plan'),
    url(r'^review_page[/]?$', 'review_page'),
    url(r'^review_page/(?P<letter>[A-PR-WZ])$', 'review_page'),
    url(r'^degree/plan/course/$', 'add_course'),
)
