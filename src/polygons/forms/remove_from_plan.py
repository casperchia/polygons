import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan

class Remove_From_Plan_Form(forms.Form):

    def delete(self, request, program_plan, semester, year):
        subject = self.cleaned_data['subject']
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        semester_plan.delete()