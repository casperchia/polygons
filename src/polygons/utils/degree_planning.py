from django.db import connection

from polygons.models.Subject import Subject

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