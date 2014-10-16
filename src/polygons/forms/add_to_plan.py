import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject

class Add_To_Plan_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Add_To_Plan_Form, self).__init__(*args, **kwargs)

        self.fields['subject_id'] = forms.IntegerField()

    def save(self, program_plan, semester, year):
        subject_id = self.cleaned_data['subject_id']
        subject = Subject.objects.get(id=subject_id)
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        semester_plan.save()
        request.session[ADD_COURSE_SESSION_KEY].clear()
