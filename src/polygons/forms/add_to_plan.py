import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY

class Add_To_Plan_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects')
        super(Add_To_Plan_Form, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(queryset=subjects)

    # def clean(self):
    #     subject = self.cleaned_data['subject']


    def save(self, request, program_plan, semester, year):
        subject = self.cleaned_data['subject']
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        semester_plan.save()
        request.session.pop(ADD_COURSE_SESSION_KEY, False)