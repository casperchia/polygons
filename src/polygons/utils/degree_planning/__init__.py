from polygons.models.Program_Rule import Program_Rule
from polygons.models.Stream_Group_Member import Stream_Group_Member
from polygons.models.Stream_Rule import Stream_Rule
from polygons.models.Rule import Rule
from polygons.models.Subject import Subject

def expand_subject_rule(rule):
    pass

def get_core_subjects(program):
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
        subjects += expand_subject_rule(rule)
    
    return subjects