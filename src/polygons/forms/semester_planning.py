import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester import Semester

class Semester_Plan_Form(forms.Form):
    
    def save(self, program):
    	program_plan = Program_Plan.objects.get(id = program)
        semester_plan = Semester_Plan(program_plan=program_plan.id, semester = program_plan.current_semester, year= progrram_plan.current_year, subjects)
        semester_plan.save()
        
        return semester_plan