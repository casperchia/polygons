from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.utils.views import get_cse_programs
from polygons.models.Program import Program
from polygons.messages import INVALID_DEGREE
from polygons.utils.degree_planning import get_core_subjects
from polygons.utils.PageForm import PageForm
from polygons.models.Program_Plan import Program_Plan

def planner(request):
    if (request.method=='POST'):
        form = PageForm(request.POST)
        if form.is_valid():
            form = PageForm.cleaned_data['plan']
            form.save()
            return HttpResponseRedirect(reverse('planner_index', kwargs={'plan_id': form}))
    else: 
      form= PageForm()
    return render_to_response('html/planner.html',
                             {'form': form,
                             },  
                             context_instance=RequestContext(request))

def planner_index(request,plan_id):
    prgm_id = request.POST.get("prgrm_pk")
    plan = Programs_Plan.objects.get(id=plan_id)
    try:
        program = get_cse_programs().get(id=prgm_id)
        # This is only for display purposes
        subjects = get_core_subjects(program)
        subjects = subjects.order_by('code')

    except Program.DoesNotExist:
        messages.error(request, INVALID_DEGREE)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))
    return render_to_response('html/planner.html',
                             { 'program' : program,
                               'subjects' : subjects,
                               'plan' : plan,
                              },
                                context_instance=RequestContext(request))

