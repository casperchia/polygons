from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Program import Program
from polygons.models.Program_Rule import Program_Rule
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Subject import Subject

#SELECT r.id, r.name, r.min, r.max, r.description,r.acad_obj_group_id, r.type_id
#FROM polygons_rule r
#JOIN polygons_program_rule pr on (r.id = pr.rule_id)
#JOIN polygons_program p on (pr.program_id = p.id)
#WHERE p.code = '3978'
#;

def program_details(request,program_id):
    # Get the program
    cse_program = Program.objects.get(pk=program_id)
    # Get the rules for this program
    p_rules = Program_Rule.objects.filter(program=cse_program.pk)
    p_rules.order_by('rule')
    # Get list of acad_objs for stream rules
    subjects = []
    for rule in p_rules :
        r = rule.rule
        subs = Subject_Group_Member.objects.filter(acad_obj_group=r.acad_obj_group)
        for s in subs :
            print s.subject.code
        subjects.append(subs)
    
    context= {'program': cse_program,
        'rules' : p_rules,
        'subjects' : subjects}
    return render_to_response('html/program_details.html',context, 
        context_instance=RequestContext(request))
