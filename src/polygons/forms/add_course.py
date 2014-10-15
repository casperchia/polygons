import django.forms as forms

from polygons.models.Semester import Semester
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import START_YEAR

ADD_COURSE_SESSION_KEY = 'add_course'

class Add_Course_Form(forms.Form):
    
    def __init__(self, program_plan, *args, **kwargs):
        super(Add_Course_Form, self).__init__(*args, **kwargs)
        
        ids = Semester_Plan.objects.filter(program_plan=program_plan).values_list('semester', flat=True)
        choices = [(s.id, s.abbreviation) for s in Semester.objects.filter(id__in=ids)]
        self.fields['semester'] = forms.ChoiceField(choices)
        
        self.fields['year'] = forms.IntegerField(min_value=START_YEAR,
                                                 max_value=program_plan.current_year)

    def save(self, request, program_plan_id):
        semester = self.cleaned_data['semester']
        year = self.cleaned_data['year']
        
        data = {
                'semester_id' : semester,
                'year' : year,
                'program_plan_id' : program_plan_id
        }
        
        request.session[ADD_COURSE_SESSION_KEY] = data
        request.session.save()