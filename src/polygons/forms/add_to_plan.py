import django.forms as forms
from django.db.models import Sum

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import Program_Plan
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY
from polygons.messages import UOC_LIMIT_EXCEEDED
from polygons.utils.views import MAX_SEMESTER_UOC
from polygons.messages import SEMESTER_UOC_LIMIT

class Add_To_Plan_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects')

        self.program_plan = kwargs.pop('program_plan')
        self.semester = kwargs.pop('semester')
        self.year = kwargs.pop('year')
        super(Add_To_Plan_Form, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(queryset=subjects)

    def clean(self):
        new_subject = self.cleaned_data['subject']
        subjects_taken = Semester_Plan.objects.filter(program_plan=self.program_plan, semester=self.semester, year=self.year)
        prg_uoc = self.program_plan.uoc_tally
        prg_uoc += new_subject.uoc
        
        uoc_sum = subjects_taken.aggregate(uoc_sum=Sum('subject__uoc')).get('uoc_sum', 0) or 0
        
        uoc =  uoc_sum + new_subject.uoc
        if uoc > MAX_SEMESTER_UOC:
            raise forms.ValidationError(SEMESTER_UOC_LIMIT)
        
        if prg_uoc > self.program_plan.program.uoc :
            raise forms.ValidationError(UOC_LIMIT_EXCEEDED)
            
            
    def save(self, request, program_plan, semester, year):
        subject = self.cleaned_data['subject']
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        prg_plan = semester_plan.program_plan
        prg_plan.uoc_tally += subject.uoc
        prg_plan.save()
        semester_plan.save()
        request.session.pop(ADD_COURSE_SESSION_KEY, False)

        
        
