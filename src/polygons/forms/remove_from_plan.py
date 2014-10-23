import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject
from polygons.utils.degree_planning import get_dependent_subjects

class Remove_From_Plan_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(Remove_From_Plan_Form, self).__init__(*args, **kwargs)
    
    def save(self, request, program_plan):
        year = program_plan.current_year
        semester = program_plan.current_semester
        subject = Subject.objects.get(id=request.POST.get("subject"))
        program_plan.uoc_tally -= subject.uoc
        dependent_subjects = get_dependent_subjects(program_plan, subject)
        for s in dependent_subjects:
            program_plan.uoc_tally -= s.uoc
            
        print program_plan.uoc_tally
        semester_plan = Semester_Plan.objects.filter(program_plan=program_plan, year=year, 
                                                     semester=semester, subject=dependent_subjects)
        semester_plan.delete()
        semester_plan = Semester_Plan.objects.filter(program_plan=program_plan, year=year, 
                                                     semester=semester, subject=subject)
        semester_plan.delete()