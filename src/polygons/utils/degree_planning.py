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
from polygons.models.Subject_Pattern import Subject_Pattern
from polygons.models.Subject_Pattern_Cache import Subject_Pattern_Cache
from polygons.models.Program_Group_Member import Program_Group_Member
from polygons.models.Program import Program

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
    subject_pattern = Subject_Pattern.objects.get(pattern=pattern)
    ids = Subject_Pattern_Cache.objects.filter(subject_pattern=subject_pattern).values_list('subject', flat=True)
    subjects = Subject.objects.filter(id__in=ids)
    
    if pattern == 'GENG####':
        subject_ids = []
        for subject in subjects:
            if get_faculty(subject.offered_by) != faculty:
                subject_ids.append(subject.id)
        subjects = Subject.objects.filter(id__in=subject_ids)
        
    return subjects

def _expand_clean_program_pattern(pattern):
    return Program.objects.filter(code__regex=pattern)

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

def _expand_program_pattern(pattern):
    match = re.search(r'([^/]+)/F=(!?)([a-zA-Z]+)', pattern)
    if match:
        (clean_pattern, negation, org_unit_code) = match.groups()
        programs = _expand_clean_program_pattern(clean_pattern)
        constraint_faculty = get_faculty(Org_Unit.objects.get(code=org_unit_code))
        program_ids = []
        if negation:
            for program in programs:
                if get_faculty(program.offered_by) != constraint_faculty:
                    program_ids.append(program.id)
        else:
            for program in programs:
                if get_faculty(program.offered_by) == constraint_faculty:
                    program_ids.append(program.id)
        return program_ids
    elif re.search(r'^!', pattern):
        negated_programs = _expand_clean_program_pattern(pattern[1:])
        programs = Program.objects.all().exclude(id__in=negated_programs.values_list('id', flat=True))
    else:
        programs = _expand_clean_program_pattern(pattern)
        
    return programs.values_list('id', flat=True)

def _expand_subject_patterns(patterns, faculty):
    subjects = []
    patterns = re.sub(r';', ',', patterns)
    
    for pattern in patterns.split(','):
        subjects = list(chain(subjects, _expand_subject_pattern(pattern, faculty)))
    
    return subjects

def _expand_program_patterns(patterns):
    programs = []
    patterns = re.sub(r';', ',', patterns)
    
    for pattern in patterns.split(','):
        programs = list(chain(programs, _expand_program_pattern(pattern)))
    
    return programs

def _gen_acad_obj_groups(rule):
    curr_acad_obj_group =  Acad_Obj_Group.objects.get(id=rule.acad_obj_group.id)
    yield curr_acad_obj_group
    while curr_acad_obj_group.parent != None:
        curr_acad_obj_group = curr_acad_obj_group.parent
        yield curr_acad_obj_group

def expand_subject_rule(rule, faculty):
    subject_ids = []
    
    for acad_obj_group in _gen_acad_obj_groups(rule):
        if acad_obj_group.enumerated:
            member_ids = Subject_Group_Member.objects.filter(acad_obj_group=acad_obj_group).values_list('subject', flat=True)
            subject_ids = list(chain(subject_ids, member_ids))
        else:
            subject_ids = list(chain(subject_ids,
                                     _expand_subject_patterns(acad_obj_group.definition,
                                                              faculty)))
    
    return subject_ids

def expand_program_rule(rule):
    program_ids = []
    
    for acad_obj_group in _gen_acad_obj_groups(rule):
        if acad_obj_group.enumerated:
            member_ids = Program_Group_Member.objects.filter(acad_obj_group=acad_obj_group).values_list('program', flat=True)
            program_ids = list(chain(program_ids, member_ids))
        else:
            program_ids = list(chain(program_ids,
                                     _expand_program_patterns(acad_obj_group.definition)))
    
    return program_ids

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
            if prereq_rule.acad_obj_group.type.name == 'program':
                prereq_ids = expand_program_rule(prereq_rule)
                if program.id not in prereq_ids:
                    meets_prereqs = False
                    break
            elif prereq_rule.acad_obj_group.type.name == 'subject':
                prereq_ids = expand_subject_rule(prereq_rule, faculty)
                if existing_subjects.filter(id__in=prereq_ids).count() < len(prereq_ids):
                    meets_prereqs = False
                    break
        if meets_prereqs:
            subject_ids.append(subject.id)
    
    return Subject.objects.filter(id__in=subject_ids)