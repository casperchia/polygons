#!/usr/bin/env python

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'comp4920.settings'
django.setup()

from django.db.models import Q

from polygons.models.Program_Rule import Program_Rule
from polygons.models.Stream_Group_Member import Stream_Group_Member
from polygons.models.Stream_Rule import Stream_Rule
from polygons.models.Rule import Rule
from polygons.models.Subject import Subject
from polygons.models.Acad_Obj_Group_Type import Acad_Obj_Group_Type
from polygons.models.Acad_Obj_Group import Acad_Obj_Group
from polygons.models.Subject_Group_Member import Subject_Group_Member
from polygons.models.Org_Unit_Group import Org_Unit_Group
from polygons.models.Org_Unit import Org_Unit
from polygons.models.Course import Course
from polygons.models.Subject_Prereq import Subject_Prereq

import re
from itertools import chain
import pickle

CACHE = {}

def get_faculty(org_unit):
    org_units = [org_unit]
    
    while org_units:
        curr_org_unit = org_units.pop(0)
        
        if curr_org_unit and curr_org_unit.type.name == 'Faculty':
            return curr_org_unit
        
        ids = Org_Unit_Group.objects.filter(~Q(owner=curr_org_unit),
                                            member=curr_org_unit).values_list('owner', flat=True)
        org_units += Org_Unit.objects.filter(id__in=ids)
            
    return None

def _expand_clean_subject_pattern(pattern):
    try:
        ids = CACHE[pattern]
    except KeyError:
        ids = False

    if ids:
        return Subject.objects.filter(id__in=ids)

    original_pattern = pattern
    pattern = re.sub(r'[{}]', '', pattern)
    pattern = re.sub(r'#', '.', pattern)
       
    if pattern in ('all', 'ALL'):
        subjects = Subject.objects.all().exclude(code__regex=r'^GEN')
    elif re.search(r'^FREE', pattern):
        pattern = re.sub(r'^FREE', '....', pattern)
        subjects = Subject.objects.filter(code__regex=pattern)
        subjects = subjects.exclude(code__regex=r'^GEN')
    elif pattern == 'GENG....':
        subjects = Subject.objects.filter(code__regex=r'^GEN')
    else:
        subjects = Subject.objects.filter(code__regex=pattern)

    CACHE[original_pattern] = list(subjects.values_list('id', flat=True))
        
    return subjects

def _expand_subject_pattern(pattern):
    match = re.search(r'([^/]+)/F=(!?)([a-zA-Z]+)', pattern)
    if match:
        (clean_pattern, negation, org_unit_code) = match.groups()
        subjects = _expand_clean_subject_pattern(clean_pattern)
        try:
            org_unit = Org_Unit.objects.get(code=org_unit_code)
        except Org_Unit.DoesNotExist:
            org_unit = None
        if org_unit:
            constraint_faculty = get_faculty(org_unit)
            subject_ids = []
            if negation:
                for subject in subjects:
                    if get_faculty(subject.offered_by) != constraint_faculty:
                        subject_ids.append(subject.id)
            else:
                for subject in subjects:
                    if get_faculty(subject.offered_by) == constraint_faculty:
                        subject_ids.append(subject.id)
        else:
            subject_ids = subjects.values_list('id', flat=True)
        return subject_ids
    elif re.search(r'^!', pattern):
        negated_subjects = _expand_clean_subject_pattern(pattern[1:])
        subjects = Subject.objects.all().exclude(id__in=negated_subjects.values_list('id', flat=True))
    else:
        subjects = _expand_clean_subject_pattern(pattern)
        
    return subjects.values_list('id', flat=True)

def _expand_subject_patterns(patterns):
    subjects = []
    patterns = re.sub(r';', ',', patterns)
    
    for pattern in patterns.split(','):
        subjects = list(chain(subjects, _expand_subject_pattern(pattern)))
    
    return subjects

def main():
    acad_obj_group_type = Acad_Obj_Group_Type.objects.get(name='subject')
    for acad_obj_group in Acad_Obj_Group.objects.filter(enumerated=False,
                                                        type=acad_obj_group_type):
        _expand_subject_patterns(acad_obj_group.definition)

    with open('~/Desktop/patterns.cache', 'w') as f:
        f.write(pickle.dumps(CACHE))

if __name__ == '__main__':
    main()
