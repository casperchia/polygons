from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.utils.views import get_cse_programs
from polygons.utils.degree_planning import get_core_subjects
from polygons.forms.program_planning import Create_Plan_Form
from polygons.models.Program import Program
from polygons.messages import INVALID_DEGREE

def program_details(request, program_id):
    try:
        program = get_cse_programs().get(id=program_id)
    except Program.DoesNotExist:
        messages.error(request, INVALID_DEGREE)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))
    
    if request.method == 'POST':
        form = Create_Plan_Form(request.POST)
        if form.is_valid():
            program_plan = form.save(program)
            return HttpResponseRedirect(reverse('polygons.views.program_plan',
                                                args=[program_plan.id]))
    else:
        form = Create_Plan_Form()
    
    subjects = get_core_subjects(program)
    subjects = subjects.order_by('code')
    
    return render_to_response('html/program_details.html', 
                              {
                                'program' : program,
                                'core_subjects' : subjects,
                                'form' : form
                              }, 
                              context_instance=RequestContext(request))
