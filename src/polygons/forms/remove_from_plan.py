import django.forms as forms
from django.db.models import Sum

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject
from polygons.utils.degree_planning import get_dependent_subjects

class Remove_From_Plan_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject')
        self.program_plan = kwargs.pop('program_plan')
        super(Remove_From_Plan_Form, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(queryset=subject)
        
    def clean(self):
        subject = self.cleaned_data['subject']
        dependent_subjects = get_dependent_subjects(self.program_plan, subject)
        uoc_removed = dependent_subjects.aggregate(uoc_removed=Sum('uoc'))
        self.program_plan.uoc_tally -= uoc_removed
        self.program_plan.uoc_tally -= subject.uoc
    
    def save(self, request, program_plan):
        subject = self.cleaned_data['subject']
        dependent_subjects = get_dependent_subjects(program_plan, subject)
            
        Semester_Plan.objects.filter(program_plan=program_plan, 
                                     subject=dependent_subjects).delete()
        Semester_Plan.objects.filter(program_plan=program_plan, 
                                                     subject=subject).delete()