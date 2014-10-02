from django.shortcuts import render_to_response
from django.template import RequestContext

def planner(request):
    return render_to_response('html/planner.html', 
        context_instance=RequestContext(request))
