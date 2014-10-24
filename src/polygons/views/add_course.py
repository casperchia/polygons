from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from polygons.models.Semester import Semester
from polygons.models.Program_Plan import Program_Plan
from polygons.messages import INVALID_ADD_COURSE_DATA
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY
from polygons.utils.degree_planning import get_program_subjects
from polygons.forms.add_course import Filter_Subjects_Form
from polygons.forms.add_to_plan import Add_To_Plan_Form
from polygons.forms.back_to_plan import Back_To_Plan_Form

def course_listing(request):
    try:
        add_course_data = request.session[ADD_COURSE_SESSION_KEY]
    except KeyError:
        messages.error(request, INVALID_ADD_COURSE_DATA)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    program_plan = Program_Plan.objects.get(id=add_course_data['program_plan_id'])
    semester = Semester.objects.get(id=add_course_data['semester_id'])

    subject_list = get_program_subjects(program_plan, add_course_data['year'],
                                        semester)
    
    if request.method == 'POST':
        filter_form = Filter_Subjects_Form(request.POST)
        if filter_form.is_valid():
            subject_list = filter_form.save(subject_list)
    else:
        filter_form = Filter_Subjects_Form()
        
    subject_list = subject_list.order_by('code')

    return render_to_response('html/add_course.html',
                             {
                                'subject_list' : subject_list,
                                'filter_form' : filter_form
                             },
                             context_instance=RequestContext(request))

def add_course(request):
    try:
        add_course_data = request.session[ADD_COURSE_SESSION_KEY]
    except KeyError:
        messages.error(request, INVALID_ADD_COURSE_DATA)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    program_plan = Program_Plan.objects.get(id=add_course_data['program_plan_id'])
    semester = Semester.objects.get(id=add_course_data['semester_id'])
    year = add_course_data['year']
    subject_list = get_program_subjects(program_plan, year, semester)
    
    if request.method == 'POST':

        form = Add_To_Plan_Form(request.POST, subjects=subject_list, program_plan=program_plan, semester=semester, year=year)
        if form.is_valid():
            form.save(request, program_plan, semester, year)
            return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                                args=[program_plan.id]))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            return HttpResponseRedirect(reverse('polygons.views.course_listing'))

    return HttpResponseRedirect(reverse('polygons.views.course_listing'))

def back_to_plan(request):
    try:
        add_course_data = request.session[ADD_COURSE_SESSION_KEY]
    except KeyError:
        messages.error(request, INVALID_ADD_COURSE_DATA)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    program_plan_id = add_course_data['program_plan_id']

    if request.method == 'POST':
        form = Back_To_Plan_Form(request.POST)
        form.save(request)

    return HttpResponseRedirect(reverse('polygons.views.program_plan', args=[program_plan_id]))