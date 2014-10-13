from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.messages import INVALID_PROGRAM_PLAN

def program_plan(request, program_plan_id):
    try:
        program_plan = Program_Plan.objects.get(id=program_plan_id)
    except Program_Plan.DoesNotExist:
        messages.error(request, INVALID_PROGRAM_PLAN)
        return HttpResponseRedirect(reverse('polygons.views.index'))
    
    return render_to_response('html/program_plan.html',
                             {
                                'program_plan' : program_plan
                             },  
                             context_instance=RequestContext(request))
