from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.messages import INVALID_PROGRAM_PLAN
from polygons.forms.add_course import Add_Course_Form


def program_plan(request, program_plan_id):
    try:
        program_plan = Program_Plan.objects.get(id=program_plan_id)
    except Program_Plan.DoesNotExist:
        messages.error(request, INVALID_PROGRAM_PLAN)
        return HttpResponseRedirect(reverse('polygons.views.index'))
    
    current_year = program_plan.current_year
    current_semester = program_plan.current_semester.id
    subject_list = Semester_Plan.objects.filter(program_plan=program_plan_id)

    if request.method == 'POST':
        form = Add_Course_Form(request.POST, program_plan=program_plan)
        if form.is_valid():
            form.save(request, program_plan_id)
            return HttpResponseRedirect(reverse('polygons.views.add_course'))
    else:
        form = Add_Course_Form(program_plan=program_plan)
    
    return render_to_response('html/program_plan.html',
                             {
                                'program_plan' : program_plan, 
                                'no_of_year' : range(1, current_year+1),
                                'subject_list' : subject_list,
                                'final_year' : current_year,
                                'final_semester' : current_semester
                             },  
                             context_instance=RequestContext(request))