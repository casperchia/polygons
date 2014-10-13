import django.forms as forms

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester import Semester

class Create_Plan_Form(forms.Form):
    
    def save(self, program):
        semester = Semester.objects.get(abbreviation='S1')
        program_plan = Program_Plan(program=program, current_semester=semester)
        program_plan.save()
        
        return program_plan