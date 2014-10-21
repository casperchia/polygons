from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.messages import INVALID_PROGRAM_PLAN
from polygons.forms.add_course import Add_Course_Form
from polygons.forms.remove_from_plan import Remove_From_Plan_Form
from polygons.utils.degree_planning import get_program_subjects


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

def remove_course(request, program_plan_id):
    
    try:
        program_plan = Program_Plan.objects.get(id=program_plan_id)
    except Program_Plan.DoesNotExist:
        return HttpResponseRedirect(reverse('polygons.views.index'))

    current_year = program_plan.current_year
    current_semester = program_plan.current_semester.id
    subject_list = get_program_subjects(program_plan, current_semester)

    if request.method == 'POST':
        form = Remove_From_Plan_Form(request.POST, subjects=subject_list)
        if form.is_valid():
            form.save(program_plan=program_plan, semester=current_semester, year=current_year)
            return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                            args=[program_plan.id]))
        else:
            form = Remove_From_Plan_Form(subjects=subject_list)
    
    return render_to_response('html/program_plan.html', 
                             {
                                'program_plan' : program_plan
                             },  
                             context_instance=RequestContext(request))