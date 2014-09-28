from django.shortcuts import render_to_response
from django.template import RequestContext

def program_details(request, program_id):
    return render_to_response('html/program_details.html', 
                              {
                                'programs' : programs
                              }, 
                              context_instance=RequestContext(request))
