from django.db import connection

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

def get_program_subjects(program_plan, semester):
    subjects = Semester_Plan.objects.filter(program_plan=program_plan).values_list('semester', flat=True)
    
    with connection.cursor() as cursor:
        cursor.execute('select get_program_subjects(%s, %s, %s)',
                       [program_plan.program_id, semester.id, subjects])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)
