import django.forms as forms

from polygons.models.Semester import Semester
from polygons.models.Career import Career
from polygons.models.Subject_Area import Subject_Area
from polygons.models.Program_Plan import START_YEAR
from polygons.messages import SUBJECT_FILTRATION_REQUIRED

import string

ADD_COURSE_SESSION_KEY = 'add_course'

class Add_Course_Form(forms.Form):
    
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    
    def __init__(self, *args, **kwargs):
        program_plan = kwargs.pop('program_plan')
        super(Add_Course_Form, self).__init__(*args, **kwargs)
        self.fields['year'] = forms.IntegerField(min_value=START_YEAR,
                                                 max_value=program_plan.current_year)

    def save(self, request, program_plan_id):
        semester = self.cleaned_data['semester']
        year = self.cleaned_data['year']
        
        data = {
                'semester_id' : semester.id,
                'year' : year,
                'program_plan_id' : program_plan_id
        }
        
        request.session[ADD_COURSE_SESSION_KEY] = data
        request.session.save()
        
class Filter_Subjects_Form(forms.Form):
    
    careers = forms.ModelMultipleChoiceField(queryset=Career.objects.all(),
                                             required=False)
    subject_areas = forms.ModelMultipleChoiceField(queryset=Subject_Area.objects.all(),
                                                   required=False)
    
    def __init__(self, *args, **kwargs):
        super(Filter_Subjects_Form, self).__init__(*args, **kwargs)
        
        choices = [(l, l) for l in list(string.uppercase)]
        self.fields['letters'] = forms.MultipleChoiceField(choices=choices)
        self.fields['letters'].required = False
        
    def clean(self):
        careers = self.cleaned_data.get('careers', False)
        subject_areas = self.cleaned_data.get('subject_areas', False)
        letters = self.cleaned_data.get('letters', False)
        
        if not careers and not subject_areas and not letters:
            raise forms.ValidationError(SUBJECT_FILTRATION_REQUIRED)
        
    def save(self, subjects):
        careers = self.cleaned_data.get('careers', False)
        if careers:
            subjects = subjects.filter(career__in=careers)
            
        subject_areas = self.cleaned_data.get('subject_areas', False)
        if subject_areas:
            subjects = subjects.filter(subject_area__in=subject_areas)
            
        letters = self.cleaned_data.get('letters', False)
        if letters:
            regex = r'^[' + ''.join(letters) + ']'
            subjects = subjects.filter(code__regex=regex)
            
        return subjects