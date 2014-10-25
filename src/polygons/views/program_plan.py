from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Subject import Subject
from polygons.messages import INVALID_PROGRAM_PLAN
from polygons.messages import PROGRAM_PLAN_DELETED
from polygons.messages import COURSE_DELETED
from polygons.messages import SEMESTER_DELETED
from polygons.forms.add_course import Add_Course_Form
from polygons.forms.remove_from_plan import Remove_From_Plan_Form
from polygons.forms.program_planning import Delete_Program_Plan_Form
from polygons.forms.semester import New_Semester_Form
from polygons.forms.semester import Remove_Semester_Form
from polygons.utils.views import render_to_pdf
from polygons.utils.views import get_formatted_plan
from polygons.utils.views import MAX_SEMESTER_UOC
from polygons.utils.degree_planning import get_dependent_subjects

from functools import wraps
import json

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
def new_semester(request,program_plan):
    if request.method == 'POST':
        form = New_Semester_Form(request.POST)
        if form.is_valid():
            form.save(program_plan)
    return  HttpResponseRedirect(reverse('polygons.views.program_plan',
                                         args=[program_plan.id]))

@get_valid_program_plan
def program_plan(request, program_plan):
    program_finished = (program_plan.uoc_tally >= program_plan.program.uoc)
    
    if request.method == 'POST':
        form = Add_Course_Form(request.POST, program_plan=program_plan)
        if form.is_valid():
            form.save(request, program_plan.id)
            return HttpResponseRedirect(reverse('polygons.views.course_listing'))    
    else:
        form = Add_Course_Form(program_plan=program_plan)
    
    plan_years = get_formatted_plan(program_plan)

    return render_to_response('html/program_plan.html',
                             {
                                'program_plan' : program_plan, 
                                'plan_years' : plan_years,
                                'MAX_SEMESTER_UOC' : MAX_SEMESTER_UOC,
                                'finished' : program_finished
                             },  
                             context_instance=RequestContext(request))


@get_valid_program_plan
def remove_course(request, program_plan):
    if request.method == 'POST':
        form = Remove_From_Plan_Form(request.POST, program_plan=program_plan)
        if form.is_valid():
            form.save()
            messages.info(request, COURSE_DELETED)
    
    return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                        args=[program_plan.id]))
    
def fetch_dependent_subjects(request, program_plan_id, subject_id):
    response_data = {'subjects' : []}
    
    valid_data = True
    
    try:
        program_plan = Program_Plan.objects.get(id=program_plan_id)
    except Program_Plan.DoesNotExist:
        valid_data = False
        
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        valid_data = False
            
    if valid_data:
        for subject in get_dependent_subjects(program_plan,
                                              subject).order_by('code'):
            response_data['subjects'].append(str(subject))
    
    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')
    
@get_valid_program_plan
def delete_program_plan(request, program_plan):
    if request.method == 'POST':
        form = Delete_Program_Plan_Form()
        form.save(program_plan)
        messages.info(request, PROGRAM_PLAN_DELETED)
    return HttpResponseRedirect(reverse('polygons.views.index'))

@get_valid_program_plan
def program_plan_to_pdf(request, program_plan):
    plan_years = get_formatted_plan(program_plan)
    
    return render_to_pdf('pdf/program_plan.html',
                         {
                            'program_plan' : program_plan,
                            'plan_years' : plan_years
                         },
                         str(program_plan.program))

@get_valid_program_plan
def remove_semester(request, program_plan):
    if request.method == 'POST':
        form = Remove_Semester_Form(request.POST, program_plan=program_plan)
        if form.is_valid():
            form.save()
            messages.info(request, SEMESTER_DELETED)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                        args=[program_plan.id]))