from django.db import connection
from django.db.models import Q
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
    past_subjects = subjects.exclude(year__gte=year,
                                     semester__abbreviation__gte=semester.abbreviation)
    
    with connection.cursor() as cursor:
        cursor.execute('select get_program_subjects(%s, %s, %s, %s, %s, %s)',
                       [program_plan.program_id, semester.id,
                        list(subjects.values_list('subject', flat=True)),
                        list(past_subjects.values_list('subject', flat=True)),
                        MAX_SEMESTER_UOC - uoc_tally,
                        list(semester_subjects.values_list('subject',
                                                           flat=True))])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.select_related('offered_by').filter(id__in=subject_ids)

def get_dependent_subjects(program_plan, pending_subject):
    existing_subjects = Semester_Plan.objects.filter(~Q(subject=pending_subject),
                                                     program_plan=program_plan).values_list('subject',
                                                                                            flat=True)
    
    with connection.cursor() as cursor:
        cursor.execute('select get_dependent_subjects(%s, %s, %s)',
                       [program_plan.program_id, pending_subject.id,
                        list(existing_subjects)])
        results = cursor.fetchall()
    
    if results:
        subject_ids = [item[0] for item in results]
    else:
        subject_ids = []
    
    return Subject.objects.filter(id__in=subject_ids)
