import django.forms as forms

from polygons.models.Semester import Semester
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import START_YEAR
from polygons.messages import NON_EMPTY_SEMESTER
from polygons.messages import CANNOT_REMOVE_FIRST_SEMESTER
from polygons.messages import MAX_YEAR_LIMIT

MAX_YEARS = 10

class New_Semester_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        self.program_plan = kwargs.pop('program_plan')
        super(New_Semester_Form, self).__init__(*args, **kwargs)

    def clean(self):
        current_semester = self.program_plan.current_semester
        semester2 = Semester.objects.get(abbreviation='S2')
        current_year = self.program_plan.current_year
        if (current_year == MAX_YEARS and current_semester == semester2):
            raise forms.ValidationError(MAX_YEAR_LIMIT)

    def save(self):
        semester1 = Semester.objects.get(abbreviation='S1')
        semester2 = Semester.objects.get(abbreviation='S2')
        if (self.program_plan.current_semester == semester2):
            self.program_plan.current_semester = semester1
            self.program_plan.current_year += 1
        else:
            self.program_plan.current_semester = semester2
        self.program_plan.save() 
        
class Remove_Semester_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.program_plan = kwargs.pop('program_plan')
        super(Remove_Semester_Form, self).__init__(*args, **kwargs)
        
    def clean(self):
        if Semester_Plan.objects.filter(program_plan=self.program_plan,
                                        year=self.program_plan.current_year,
                                        semester=self.program_plan.current_semester).exists():
            raise forms.ValidationError(NON_EMPTY_SEMESTER)
        else:
            if self.program_plan.current_year == START_YEAR:
                semester1 = Semester.objects.get(abbreviation='S1')
                if self.program_plan.current_semester == semester1:
                    raise forms.ValidationError(CANNOT_REMOVE_FIRST_SEMESTER)

    def save(self):
        semester1 = Semester.objects.get(abbreviation='S1')
        semester2 = Semester.objects.get(abbreviation='S2')
        if self.program_plan.current_semester == semester1:
            self.program_plan.current_year -= 1
            self.program_plan.current_semester = semester2
        else:
            self.program_plan.current_semester = semester1
            
        self.program_plan.save()