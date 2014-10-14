from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.forms.add_course import Semester_Plan_Form
from polygons.messages import INVALID_PROGRAM_PLAN

def add_course(request):
   try:
        program_plan_id = request.session['program_plan_id']
        program_id = request.session['program_id']    
        program = Program.objects.get(id=program_id)
        semester_id = request.session['semester_id']
        semester = Semester.objects.get(id=semester_id)

        # Does get_program_subjects() take a list of subjects, or subject ids?
        # subjects_id = request.session['subjects_id']
        # subjects = Subject.objects.filter()
        subject_list = get_program_subjects(program, semester)
        # subject_list = get_program_subjects(program, semester, existing_subjects)

   except Program.DoesNotExist:
        messages.error(request, INVALID_DEGREE)
        return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                            args=[program_plan_id]))
   except Semester.DoesNotExist:
        messages.error(request, INVALID_SEMESTER)
        return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                            args=[program_plan_id]))
   except Subject.DoesNotExist:
        messages.error(request, INVALID_SUBJECT)
        return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                            args=[program_plan_id]))
    
   # subject_list = Semester_Plan.objects.filter(program=program_id)
   # if request.method == 'POST':
   #     form = Semester_Plan_Form(request.POST)
   #     if form.is_valid():
   #         semester_plan = form.save(program,subject)
   #         return HttpResponseRedirect('html/course_list.html')
   # else:
   #      form = Semester_Plan_Form() 
   return render_to_response('html/add_course.html',
                             {
                                'subject_list' : subject_list
                             },
                             context_instance=RequestContext(request))
