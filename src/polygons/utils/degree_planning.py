from polygons.models.Program_Rule import Program_Rule
from polygons.models.Stream_Group_Member import Stream_Group_Member
from polygons.models.Stream_Rule import Stream_Rule
from polygons.models.Rule import Rule
from polygons.models.Subject import Subject
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Org_Unit_Group import Org_Unit_Group
from polygons.models.Org_Unit import Org_Unit

import re

def get_faculty(org_unit):
    org_units = [org_unit]
    
    while org_units:
        curr_org_unit = org_units.pop(0)
        
        if curr_org_unit.type == 'Faculty':
            return curr_org_unit
        
        ids = Org_Unit_Group.objects.filter(member=org_unit).values_list('owner', flat=True)
        org_units += Org_Unit.objects.filter(id__in=ids)
            
    return None

def _expand_clean_subject_pattern(pattern, faculty):
    pattern = re.sub(r'[{}]', '', pattern)
    pattern = re.sub(r'#', '.', pattern)
        
    '''
    * Handle !, at the beginning of a normal pattern, or before a faculty constraint
    * all, ALL, FREE#### = any course that is not a gen-ed
    * GENG#### = any gen-ed course not in home faculty
    * REGEX IT!
    '''

def _expand_subject_pattern(pattern, faculty):
    match = re.search(r'([^/]+)/F=(!?)([a-zA-Z]+)', pattern)
    if match:
        (clean_pattern, negation, org_unit_code) = match.groups()
        subjects = _expand_clean_subject_pattern(clean_pattern, faculty)
        constraint_faculty = get_faculty(Org_Unit.objects.get(code=org_unit_code))
        subject_ids = []
        if negation:
            for subject in subjects:
                if get_faculty(subject.offered_by) != constraint_faculty:
                    subject_ids.append(subject.id)
        else:
            for subject in subjects:
                if get_faculty(subject.offered_by) == constraint_faculty:
                    subject_ids.append(subject.id)
        subjects = Subject.objects.filter(id__in=subject_ids)
    elif re.search(r'^!', pattern):
        negated_subjects = _expand_clean_subject_pattern(pattern[1:], faculty)
        subjects = Subject.objects.all().exclude(id__in=negated_subjects.values_list('id', flat=True))
    else:
        subjects = _expand_clean_subject_pattern(pattern, faculty)
        
    return subjects

def expand_subject_patterns(patterns, faculty):
    subjects = Subject.objects.none()
    patterns = re.sub(r';', ',', patterns)
    
    for pattern in patterns.split(','):
        subjects += _expand_subject_pattern(pattern, faculty)
    
    return subjects

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
            subjects += expand_subject_patterns(acad_obj_group.definition,
                                                faculty)
    
    return subjects

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