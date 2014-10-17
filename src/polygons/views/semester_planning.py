from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.views.program_details import program_details
from polygons.forms.semester_planning import Semester_Plan_Form
from polygons.models.Program_Plan import Program_Plan
from polygons.messages import INVALID_DEGREE

def semester_planning(request,program_plan_id):
    try:
        program = Program_Plan.objects.get(id=program_plan_id)

    except Program_Plan.DoesNotExist:
        messages.error(request, INVALID_PROGRAM_PLAN)
        return HttpResponseRedirect(reverse('polygons.views.index'))
    
    if request.method == 'POST':
        form = Semester_Plan_Form(request.POST)
        if form.is_valid():
            semester_plan = form.save(program_plan_id)
            return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                                args=[program.id]))
    else:
	    form = Semester_Plan_Form()
	    return render_to_response('html/program_details.html',  
	    	                  {
	    	                       'program' : program
	    	                  },
                              context_instance=RequestContext(request))