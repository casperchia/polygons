from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member

# SELECT p.id,p.name,p.degree_id,p.offered_by_id,o.id
# FROM polygons_program p
# JOIN polygons_org_unit o on (o.id = p.offered_by_id)
# WHERE o.id = 89
# ;


#SELECT p.id,p.name,p.degree_id,p.offered_by_id     
#FROM polygons_program p
#JOIN polygons_program_group_member o on (o.program_id = p.id)
#JOIN polygons_acad_obj_group a on (o.acad_obj_group_id = a.id)
#WHERE a.id = 20382
#;


def degree_planner(request):
    # 89 is the Org_Unit id for Computer Science and Engineering
    cse_programs = Program_Group_Member.objects.filter(acad_obj_group = '20382')
    
    # List of degree values
    d_ids = []
    for program in cse_programs :
        d_ids.append(program.program)
       
        
    
    #cse_degrees = Degree.objects.filter(pk__in=d_ids)
    context = {'degree_list': d_ids}
    return render_to_response('html/degree_planner.html', context, 
        context_instance=RequestContext(request))
