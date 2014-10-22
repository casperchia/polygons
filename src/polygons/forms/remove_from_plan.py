import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject

class Remove_From_Plan_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(Remove_From_Plan_Form, self).__init__(*args, **kwargs)
    
    def save(self, request, program_plan):
        year = program_plan.current_year
        semester = program_plan.current_semester
        subject = Subject.objects.get(id=request.POST.get("subject"))
        semester_plan = Semester_Plan.objects.filter(program_plan=program_plan, year=year, 
                                                     semester=semester, subject=subject)
        semester_plan.delete()