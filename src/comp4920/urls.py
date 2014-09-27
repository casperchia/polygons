from django.conf.urls import patterns, url

urlpatterns = patterns('polygons.views',
    url(r'^$', 'index'),
)
