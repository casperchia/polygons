from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
    url(r'^degrees/$', 'degree_list'),
    url(r'^degree/(?P<program_id>\d+)/$', 'program_details'),
    url(r'^degree/plan/(?P<program_plan_id>\d+)/$', 'program_plan'),
    url(r'^degree/plan/delete/(?P<program_plan_id>\d+)/$', 'delete_program_plan'),
    url(r'^degree/plan/pdf/(?P<program_plan_id>\d+)/$', 'program_plan_to_pdf'),
    url(r'^degree/plan/courses/$', 'course_listing'),
    url(r'^degree/plan/course/add/$', 'add_course'),
    url(r'^degree/plan/course/back/$', 'back_to_plan'),
    url(r'^degree/plan/semester/(?P<program_plan_id>\d+)/$', 'new_semester'),
    url(r'^degree/plan/remove-course/(?P<program_plan_id>\d+)/$', 'remove_course'),
    url(r'^degree/plan/dependent-subjects/(?P<program_plan_id>\d+)/(?P<subject_id>\d+)/',
        'fetch_dependent_subjects')
)

handler404 = 'polygons.views.http.response_404'
handler500 = 'polygons.views.http.response_500'
