from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degrees/$', 'degree_list'),
    url(r'^degree/(?P<program_id>\d+)/$', 'program_details'),
    url(r'^degree/plan/(?P<program_plan_id>\d+)/$', 'program_plan'),
    url(r'^degree/plan/delete/(?P<program_plan_id>\d+)/$',
        'delete_program_plan'),
    url(r'^degree/plan/pdf/(?P<program_plan_id>\d+)/$', 'program_plan_to_pdf'),
    url(r'^review_page[/]?$', 'review_page'),
    url(r'^degree/plan/courses/$', 'course_listing'),
    url(r'^degree/plan/course/add/$', 'add_course'),
    url(r'^review_page/(?P<filter>[A-Z]{1,4})$', 'review_page'),
    url(r'^degree/plan/remove/(?P<program_plan_id>\d+)/$', 'remove_course')
)
