import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester import Semester
from polygons.messages import MAX_YEAR_LIMIT


MAX_YEARS = 10

class New_Semester_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.program_plan = kwargs.pop('program_plan')
        super(New_Semester_Form, self).__init__(*args, **kwargs)

    def save(self):
        semester1 = Semester.objects.get(abbreviation='S1')
        semester2 = Semester.objects.get(abbreviation='S2')
        if (self.program_plan.current_semester == semester2):
            self.program_plan.current_semester = semester1
            self.program_plan.current_year += 1
        else:
            self.program_plan.current_semester = semester2
        self.program_plan.save() 
        
    def clean(self):
        current_semester = self.program_plan.current_semester
        semester2 = Semester.objects.get(abbreviation='S2')
        current_year = self.program_plan.current_year
        if (current_year == MAX_YEARS and current_semester == semester2):
            raise forms.ValidationError(MAX_YEAR_LIMIT)
