from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.utils.views import get_cse_programs
from polygons.models.Program import Program
from polygons.messages import INVALID_DEGREE
from polygons.utils.degree_planning import get_core_subjects

def planner(request):
    prgm_id = request.POST.get("prgrm_pk")
    try:
        program = get_cse_programs().get(id=prgm_id)
        # This is only for display purposes
        subjects = get_core_subjects(program)
        subjects = subjects.order_by('code')
        
    except Program.DoesNotExist:
        messages.error(request, INVALID_DEGREE)
        return HttpResponseRedirect(reverse('polygons.views.degree_list'))

    return render_to_response('html/planner.html',
                              {
                                'program' : program,
                                'subjects' : subjects
                              }, 
                                context_instance=RequestContext(request))
