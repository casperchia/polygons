import django.forms as forms

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Semester import Semester

class Add_Course(forms.Form):
    semester = forms.IntegerField()
    year = forms.IntegerField()

    def save(self,program_plan):
        year = self.cleaned_data['year']

        # need choice field for semester to validate input
        semester = self.cleaned_data['semester']

        # semester_plan = Semester_plan(program=program,subject= subject)
        # semester_plan.save()

        return semester_plan

# save semester, year and program_plan id into user session
# add them to session
