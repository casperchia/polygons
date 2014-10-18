import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import Program_Plan
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY

class Add_To_Plan_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects')
        self.prg_plan = kwargs.pop('prg_plan')
        super(Add_To_Plan_Form, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(queryset=subjects)

    # This is where the course gets added to the plan
    def save(self, request, program_plan, semester, year):
        subject = self.cleaned_data['subject']
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        prg_plan = semester_plan.program_plan
        prg_plan.uoc_tally += subject.uoc
        prg_plan.save()
        semester_plan.save()
        request.session.pop(ADD_COURSE_SESSION_KEY, False)
        
        
    def clean(self):
        
        subject = self.cleaned_data['subject']
        current_uoc = self.prg_plan.uoc_tally
        current_uoc += subject.uoc
        if current_uoc > self.prg_plan.program.uoc :
            raise forms.ValidationError("Cannot add course to plan as "
                "you have exceeded the program UOC limit.")
        
        
