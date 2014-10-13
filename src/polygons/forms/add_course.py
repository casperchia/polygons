import django.forms as forms

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Semester import Semester

class Semester_Plan_Form(forms.Form):
    semester = forms.IntegerField()

    def save(self,program,subject):
        semester_plan = Semester_plan(program=program,subject= subject)
        semester_plan.save()

        return semester_plan

