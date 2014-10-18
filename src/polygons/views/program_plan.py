from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.messages import INVALID_PROGRAM_PLAN
from polygons.messages import PROGRAM_PLAN_DELETED
from polygons.forms.add_course import Add_Course_Form
from polygons.forms.program_planning import Delete_Program_Plan_Form

from functools import wraps

def get_valid_program_plan(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        program_plan_id = kwargs.pop('program_plan_id')
        
        try:
            program_plan = Program_Plan.objects.get(id=program_plan_id)
        except Program_Plan.DoesNotExist:
            messages.error(request, INVALID_PROGRAM_PLAN)
            return HttpResponseRedirect(reverse('polygons.views.index'))
        
        kwargs['program_plan'] = program_plan
        
        return view(request, *args, **kwargs)
    
    return wrapper

@get_valid_program_plan
def program_plan(request, program_plan):
    current_year = program_plan.current_year
    current_semester = program_plan.current_semester.id
    subject_list = Semester_Plan.objects.filter(program_plan=program_plan.id)

    if request.method == 'POST':
        form = Add_Course_Form(request.POST, program_plan=program_plan)
        if form.is_valid():
            form.save(request, program_plan.id)
            return HttpResponseRedirect(reverse('polygons.views.course_listing'))
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
    
@get_valid_program_plan
def delete_program_plan(request, program_plan):
    if request.method == 'POST':
        form = Delete_Program_Plan_Form()
        form.save(program_plan)
        messages.info(request, PROGRAM_PLAN_DELETED)
    
    return HttpResponseRedirect(reverse('polygons.views.index'))