import django.forms as forms

from polygons.models.Semester import Semester
from polygons.models.Career import Career
from polygons.models.Subject_Area import Subject_Area
from polygons.models.Program_Plan import START_YEAR
from polygons.messages import SUBJECT_FILTRATION_REQUIRED

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

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects')
        super(Filter_Subjects_Form, self).__init__(*args, **kwargs)
        
        career_ids = subjects.distinct('career').values_list('career',
                                                             flat=True)
        careers = Career.objects.filter(id__in=career_ids)
        self.fields['careers'] = forms.ModelMultipleChoiceField(queryset=careers,
                                                                required=False)
        
        subject_area_ids = subjects.distinct('subject_area').values_list('subject_area',
                                                                         flat=True)
        subject_areas = Subject_Area.objects.filter(id__in=subject_area_ids)
        self.fields['subject_areas'] = forms.ModelMultipleChoiceField(queryset=subject_areas,
                                                                      required=False)
        
        first_letters = {}
        for subject in subjects:
            first_letter = subject.code[0]
            first_letters[first_letter] = (first_letter, first_letter)
        self.fields['letters'] = forms.MultipleChoiceField(choices=first_letters.values())
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