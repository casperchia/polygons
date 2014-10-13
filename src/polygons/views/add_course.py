from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.forms.add_course import Semester_Plan_Form
from polygons.messages import INVALID_PROGRAM_PLAN

def add_course(request,program_plan_id):
   try:
        program = get_cse_programs().get(id=program_id)

   except Program.DoesNotExist:
        messages.error(request, INVALID_DEGREE)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))
    
   subject_list = Semester_Plan.objects.filter(program=program_id)
   if request.method == 'POST':
       form = Semester_Plan_Form(request.POST)
       if form.is_valid():
           semester_plan = form.save(program,subject)
           return HttpResponseRedirect('html/course_list.html')
   else:
        form = Semester_Plan_Form() 
   return render_to_response('html/program_plan.html',
                             {
                                'semester_plan' : semester_plan,
                             },
                             context_instance=RequestContext(request))
