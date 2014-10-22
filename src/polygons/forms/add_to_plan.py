import django.forms as forms
from django.db.models import Sum

from polygons.models.Semester_Plan import Semester_Plan
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY
from polygons.utils.views import MAX_SEMESTER_UOC
from polygons.messages import SEMESTER_UOC_LIMIT
from polygons.models.Subject import Subject


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
        uoc_dict = Semester_Plan.objects.filter(program_plan=self.program_plan, 
                                                semester=self.semester, 
                                                year=self.year).aggregate(uoc_sum=Sum('subject__uoc'))
        uoc_sum = uoc_dict.get('uoc_sum', 0) or 0
        uoc =  uoc_sum + new_subject.uoc
        if uoc > MAX_SEMESTER_UOC:
            raise forms.ValidationError(SEMESTER_UOC_LIMIT)       

    def save(self, request, program_plan, semester, year):
        subject = self.cleaned_data['subject']
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        semester_plan.save()
        request.session.pop(ADD_COURSE_SESSION_KEY, False)