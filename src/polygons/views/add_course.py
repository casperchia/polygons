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

def add_course(request):
    try:
        add_course_data = request.session[ADD_COURSE_SESSION_KEY]
    except KeyError:
        messages.error(request, INVALID_ADD_COURSE_DATA)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    program_plan = Program_Plan.objects.get(id=add_course_data['program_plan_id'])
    semester = Semester.objects.get(id=add_course_data['semester_id'])

    subject_list = get_program_subjects(program_plan, semester)

    return render_to_response('html/add_course.html',
                             {
                                'subject_list' : subject_list
                             },
                             context_instance=RequestContext(request))