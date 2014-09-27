from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Program_Group_Member import Program_Group_Member

CSE_PLANS_ID = 20382


def degree_list(request):
    members = Program_Group_Member.objects.filter(acad_obj_group=CSE_PLANS_ID).select_related('program')
    programs = [pgm.program for pgm in members]   
    
    return render_to_response('html/degree_list.html', 
                              {
                                'programs' : programs
                              }, 
                              context_instance=RequestContext(request))
