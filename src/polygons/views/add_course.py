from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from polygons.models.Semester import Semester
from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program import Program
from polygons.forms.add_course import Add_Course_Form
from polygons.messages import INVALID_ADD_COURSE_DATA
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY
from polygons.utils.degree_planning import get_program_subjects
from polygons.forms.add_to_plan import Add_To_Plan_Form

def add_course(request):
    try:
        add_course_data = request.session[ADD_COURSE_SESSION_KEY]
        
    except KeyError:
        messages.error(request, INVALID_ADD_COURSE_DATA)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    semester_id = add_course_data['semester_id']
    year = add_course_data['year']
    program_plan_id = add_course_data['program_plan_id']

    program_plan = Program_Plan.objects.get(id=program_plan_id)
    program_id = program_plan.program.id
    program = Program.objects.get(id=program_id)
    semester = Semester.objects.get(id=semester_id)

    subject_list = get_program_subjects(program_plan, semester)

    if request.method == 'POST':
        form = Add_To_Plan_Form(request.POST, subjects=subject_list)
        if form.is_valid():
            form.save(request, program_plan, semester, year)
            return HttpResponseRedirect(reverse('polygons.views.program_plan', args=[program_plan_id]))
    else:
        form = Add_To_Plan_Form(subjects=subject_list)


    return render_to_response('html/add_course.html',
                             {
                             'subject_list' : subject_list
                             },
                             context_instance=RequestContext(request))
