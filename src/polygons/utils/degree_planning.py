from django.db.models import Q

from polygons.models.Program_Rule import Program_Rule
from polygons.models.Stream_Group_Member import Stream_Group_Member
from polygons.models.Stream_Rule import Stream_Rule
from polygons.models.Rule import Rule
from polygons.models.Subject import Subject
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Org_Unit_Group import Org_Unit_Group
from polygons.models.Org_Unit import Org_Unit
from polygons.models.Course import Course
from polygons.models.Subject_Prereq import Subject_Prereq

import re
from itertools import chain

def get_faculty(org_unit):
    org_units = [org_unit]
    
    while org_units:
        curr_org_unit = org_units.pop(0)
        
        if curr_org_unit.type.name == 'Faculty':
            return curr_org_unit
        
        ids = Org_Unit_Group.objects.filter(~Q(owner=curr_org_unit),
                                            member=curr_org_unit).values_list('owner', flat=True)
        org_units += Org_Unit.objects.filter(id__in=ids)
            
    return None

def _expand_clean_subject_pattern(pattern, faculty):
    pattern = re.sub(r'[{}]', '', pattern)
    pattern = re.sub(r'#', '.', pattern)
       
    if pattern in ('all', 'ALL'):
        subjects = Subject.objects.all().exclude(code__regex=r'^GEN')
    elif re.search(r'^FREE', pattern):
        pattern = re.sub(r'^FREE', '....', pattern)
        subjects = Subject.objects.filter(code__regex=pattern)
        subjects = subjects.exclude(code__regex=r'^GEN')
    elif pattern == 'GENG####':
        subjects = Subject.objects.filter(code__regex=r'^GEN')
        subject_ids = []
        for subject in subjects:
            if get_faculty(subject.offered_by) != faculty:
                subject_ids.append(subject.id)
        subjects = Subject.objects.filter(id__in=subject_ids)
    else:
        subjects = Subject.objects.filter(code__regex=pattern)
        
    return subjects

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
        return subject_ids
    elif re.search(r'^!', pattern):
        negated_subjects = _expand_clean_subject_pattern(pattern[1:], faculty)
        subjects = Subject.objects.all().exclude(id__in=negated_subjects.values_list('id', flat=True))
    else:
        subjects = _expand_clean_subject_pattern(pattern, faculty)
        
    return subjects.values_list('id', flat=True)

def _expand_subject_patterns(patterns, faculty):
    subjects = []
    patterns = re.sub(r';', ',', patterns)
    
    for pattern in patterns.split(','):
        subjects = list(chain(subjects, _expand_subject_pattern(pattern, faculty)))
    
    return subjects

def expand_subject_rule(rule, faculty):
    subject_ids = []
    
    acad_obj_groups = [Acad_Obj_Group.objects.get(id=rule.acad_obj_group.id)]
    curr_acad_obj_group = acad_obj_groups[0]
    while curr_acad_obj_group.parent != None:
        curr_acad_obj_group = curr_acad_obj_group.parent
        acad_obj_groups.append(curr_acad_obj_group)
    
    for acad_obj_group in acad_obj_groups:
        if acad_obj_group.enumerated:
            member_ids = Subject_Group_Member.objects.filter(acad_obj_group=acad_obj_group).values_list('subject', flat=True)
            subject_ids = list(chain(subject_ids, member_ids))
        else:
            subject_ids = list(chain(subject_ids,
                                     _expand_subject_patterns(acad_obj_group.definition,
                                                              faculty)))
    
    return subject_ids

def get_core_subjects(program):
    faculty = get_faculty(program.offered_by)
    subject_ids = []
    
    program_rules = Program_Rule.objects.filter(program=program).values_list('rule', flat=True)
    core_subject_rules = Rule.objects.filter(id__in=program_rules, type__abbreviation='CC')
    ds_rules = Rule.objects.filter(id__in=program_rules, type__abbreviation='DS')
            
    for ds_rule in ds_rules:
        stream_members = Stream_Group_Member.objects.select_related('stream').filter(acad_obj_group=ds_rule.acad_obj_group)
        
        for stream in [sm.stream for sm in stream_members]:
            stream_rules = Stream_Rule.objects.filter(stream=stream).values_list('rule', flat=True)
        
        core_subject_rules = list(chain(core_subject_rules, 
                                        Rule.objects.filter(id__in=stream_rules,
                                                            type__abbreviation='CC')))
        
    for rule in core_subject_rules:
        subject_ids = list(chain(subject_ids, expand_subject_rule(rule, faculty)))
    
    return Subject.objects.filter(id__in=subject_ids)

def get_program_subjects(program, semester,
                         existing_subjects=Subject.objects.none()):
    faculty = get_faculty(program.offered_by)
    subject_ids = []
    
    program_rules = Program_Rule.objects.filter(program=program).values_list('rule', flat=True)
    subject_rules = Rule.objects.filter(~Q(type__abbreviation='DS'), id__in=program_rules)
    ds_rules = Rule.objects.filter(id__in=program_rules, type__abbreviation='DS')
    
    for ds_rule in ds_rules:
        stream_members = Stream_Group_Member.objects.select_related('stream').filter(acad_obj_group=ds_rule.acad_obj_group)
        
        for stream in [sm.stream for sm in stream_members]:
            stream_rules = Stream_Rule.objects.filter(stream=stream).values_list('rule', flat=True)
        
        subject_rules = list(chain(subject_rules, 
                                   Rule.objects.filter(id__in=stream_rules)))
        
    for rule in subject_rules:
        subject_ids = list(chain(subject_ids, expand_subject_rule(rule, faculty)))
        
    subjects = Subject.objects.filter(id__in=subject_ids)
    
    # Subjects already in the plan
    subjects = subjects.exclude(id__in=existing_subjects.values_list('id', flat=True))
    # Subjects not offered in the specified semester
    subjects = subjects.exclude(id__in=Course.objects.filter(~Q(semester=semester)).values_list('subject',
                                                                                                flat=True))
    # Subjects excluded by subjects already in the plan
    for existing_subject in existing_subjects:
        exclusion_rule = Rule.objects.get(acad_obj_group=existing_subject.excluded)
        excluded_ids = expand_subject_rule(exclusion_rule, faculty)
        subjects = subjects.exclude(id__in=excluded_ids)
    # Subjects whose prereqs have not been met
    subject_ids = []
    for subject in subjects:
        meets_prereqs = True
        prereq_rules = Subject_Prereq.objects.select_related('rule').filter(subject=subject,
                                                                            career=program.career)
        for prereq_rule in [pr.rule for pr in prereq_rules]:
            prereq_ids = expand_subject_rule(prereq_rule, faculty)
            if existing_subjects.filter(id__in=prereq_ids).count() < len(prereq_ids):
                meets_prereqs = False
                break
        if meets_prereqs:
            subject_ids.append(subject.id)
    
    return Subject.objects.filter(id__in=subject_ids)