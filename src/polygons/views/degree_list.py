from django.shortcuts import render_to_response
from django.template import RequestContext

from polygons.utils.views import get_cse_programs

def degree_list(request):
    return render_to_response('html/degree_list.html', 
                              {
                                'programs' : get_cse_programs()
                              }, 
                              context_instance=RequestContext(request))
