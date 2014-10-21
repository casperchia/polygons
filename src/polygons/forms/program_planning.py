import django.forms as forms

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester import Semester
from polygons.models.Semester_Plan import Semester_Plan

class Create_Plan_Form(forms.Form):
    
    def save(self, program):
        semester = Semester.objects.get(abbreviation='S1')
        program_plan = Program_Plan(program=program, current_semester=semester)
        program_plan.save()
        
        return program_plan
    
class Delete_Program_Plan_Form(forms.Form):
    
    def save(self, program_plan):
        Semester_Plan.objects.filter(program_plan=program_plan).delete()
        program_plan.delete()