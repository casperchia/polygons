from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.views.program_details import program_details
from polygons.forms.add_semester import New_Semester_Form
from polygons.models.Program_Plan import Program_Plan
from polygons.messages import INVALID_DEGREE

def semester_planning(request,program_plan_id):
    if request.method == 'POST':
        form = New_Semester_Form(request.POST)
        if form.is_valid():
            semester_plan = form.save(program_plan_id)
            return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                                args=[semester_plan.id]))
    else:
	    form = New_Semester_Form()
	    return render_to_response('html/program_details.html',  
	    	                  {
	    	                       'program' : program
	    	                  },
                              context_instance=RequestContext(request))