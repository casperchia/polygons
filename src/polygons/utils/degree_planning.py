from django.db import connection
from django.db.models import Sum

from polygons.models.Subject import Subject
from polygons.models.Semester_Plan import Semester_Plan
from polygons.utils.views import MAX_SEMESTER_UOC

def get_core_subjects(program):
    with connection.cursor() as cursor:
        cursor.execute('select get_core_subjects(%s)', [program.id])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)

def get_program_subjects(program_plan, year, semester):
    semester_subjects = Semester_Plan.objects.filter(program_plan=program_plan,
                                                     year=year,
                                                     semester=semester)
    uoc_tally = semester_subjects.aggregate(sum=Sum('subject__uoc')).get('sum', 0) or 0
    subjects = Semester_Plan.objects.filter(program_plan=program_plan)
    past_subjects = subjects.exclude(year=year, semester=semester)
    
    with connection.cursor() as cursor:
        cursor.execute('select get_program_subjects(%s, %s, %s, %s, %s)',
                       [program_plan.program_id, semester.id,
                        list(subjects.values_list('subject', flat=True)),
                        list(past_subjects.values_list('subject', flat=True)),
                        MAX_SEMESTER_UOC - uoc_tally])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.select_related('offered_by').filter(id__in=subject_ids)
