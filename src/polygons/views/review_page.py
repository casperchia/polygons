from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Subject import Subject
import string

def review_page(request,letter=None):

    if letter is None :
        subjects = Subject.objects.all()
    else :
        subjects = Subject.objects.filter(code__startswith=letter)
    subjects = subjects.order_by('code')
    
    alphabet = list(string.ascii_uppercase)
    
    return render_to_response('html/review_page.html',
                                {
                                    'subjects' : subjects,
                                    'alphabet' : alphabet
                                }, 
                              context_instance=RequestContext(request))
