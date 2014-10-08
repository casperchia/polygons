from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Subject import Subject

def review_page(request):

    subjects = Subject.objects.all()
    subjects = subjects.order_by('code')
    
    return render_to_response('html/review_page.html',
                                {
                                    'subjects' : subjects
                                }, 
                              context_instance=RequestContext(request))
