from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan

def display_info(request):
       program_id = request.POST.get("prgrm_pk")

       # Shouldn't we be getting a program plan based on the id as follows:
       # program_plan = Program_plan.objects.get(id=program_id)       
       
       # As opposed to this:
       program_plan = Program_plan.objects.get(program=program_id)
       semester_plan= Semester_plan.objects.get(program_plan=program_plan)
       return render_to_response('html/display.html',
                                {'program_plan' : program_plan,
                                 'semester_plan' : semester_plan
                                }
