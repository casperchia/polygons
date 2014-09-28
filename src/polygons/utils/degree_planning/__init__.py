from polygons.models.Program_Rule import Program_Rule
from polygons.models.Stream_Group_Member import Stream_Group_Member
from polygons.models.Stream_Rule import Stream_Rule
from polygons.models.Rule import Rule
from polygons.models.Subject import Subject
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Org_Unit_Group import Org_Unit_Group

def expand_subject_pattern(pattern, faculty):
    pass

def expand_subject_rule(rule, faculty):
    subjects = Subject.objects.none()
    
    acad_obj_groups = [Acad_Obj_Group.objects.get(id=rule.acad_obj_group.id)]
    curr_acad_obj_group = acad_obj_groups[0]
    while curr_acad_obj_group.parent != None:
        curr_acad_obj_group = curr_acad_obj_group.parent
        acad_obj_groups.append(curr_acad_obj_group)
    
    for acad_obj_group in acad_obj_groups:
        if acad_obj_group.enumerated:
            subject_ids = Subject_Group_Member.objects.filter(acad_obj_group=acad_obj_group).values_list('subject', flat=True)
            subjects += Subject.objects.filter(id__in=subject_ids)
        else:
            subjects += expand_subject_pattern(acad_obj_group.definition,
                                               faculty)
    
    return subjects

def get_faculty(org_unit):
    result = None
    
    if org_unit.type == 'Faculty':
        result = org_unit
    else:
        for oug in Org_Unit_Group.objects.select_related('owner').filter(member=org_unit):
            result = get_faculty(oug.owner)
            if result:
                break
        
    return result

def get_core_subjects(program):
    faculty = get_faculty(program.offered_by)
    subjects = Subject.objects.none()
    
    program_rules = Program_Rule.objects.filter(program=program).values_list('rule', flat=True)
    core_subject_rules = Rule.objects.filter(id__in=program_rules, type__abbreviation='CC')
    ds_rules = Rule.objects.filter(id__in=program_rules, type__abbreviation='DS')
            
    for ds_rule in ds_rules:
        stream_members = Stream_Group_Member.objects.select_related('stream').filter(acad_obj_group=ds_rule.acad_obj_group)
        
        for stream in [sm.stream for sm in stream_members]:
            stream_rules = Stream_Rule.objects.filter(stream=stream).values_list('rule', flat=True)
        
        core_subject_rules += Rule.objects.filter(id__in=stream_rules, type__abbreviation='CC')
        
    for rule in core_subject_rules:
        subjects += expand_subject_rule(rule, faculty)
    
    return subjects