import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester import Semester


class New_Semester_Form(forms.Form):
    
    def save(self, program):
    	program_plan = Program_Plan.objects.get(id = program)
    	semester1 = Semester.objects.get(abbreviation='S1')
    	semester2 = Semester.objects.get(abbreviation='S2')
        if (program_plan.current_semester == semester2):
        	program_plan.current_semester = semester1
        	program_plan.current_year += 1
        else:
        	program_plan.current_semester = semester2
        program_plan.save()
        return program_plan