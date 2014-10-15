from django.db import connection
from django.db.models import Q

from polygons.models.Subject import Subject
from polygons.models.Semester_Plan import Semester_Plan

def get_core_subjects(program):
    with connection.cursor() as cursor:
        cursor.execute('select get_core_subjects(%s)', [program.id])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)

def get_program_subjects(program, semester,
                         existing_subjects=[]):
    with connection.cursor() as cursor:
        cursor.execute('select get_program_subjects(%s, %s, %s)',
                       [program.id, semester.id, list(existing_subjects)])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)

def get_dependent_subjects(program_plan, pending_subject):
    existing_subjects = Semester_Plan.objects.filter(~Q(subject=pending_subject),
                                                     program_plan=program_plan).values_list('subject',
                                                                                            flat=True)
    
    with connection.cursor() as cursor:
        cursor.execute('select get_dependent_subjects(%s, %s, %s)',
                       [program_plan.program_id, pending_subject.id,
                        existing_subjects])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)