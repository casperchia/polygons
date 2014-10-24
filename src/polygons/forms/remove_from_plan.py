import django.forms as forms
from django.db.models import Sum

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject
from polygons.utils.degree_planning import get_dependent_subjects

class Remove_From_Plan_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.program_plan = kwargs.pop('program_plan')
        super(Remove_From_Plan_Form, self).__init__(*args, **kwargs)
        
        subject_ids = Semester_Plan.objects.filter(program_plan=self.program_plan).values_list('subject',
                                                                                               flat=True)
        subjects = Subject.objects.filter(id__in=subject_ids)
        
        self.fields['subject'] = forms.ModelChoiceField(queryset=subjects)
    
    def save(self):
        subject = self.cleaned_data['subject']
        dependent_subjects = get_dependent_subjects(self.program_plan, subject)
            
        Semester_Plan.objects.filter(program_plan=self.program_plan, 
                                     subject__in=dependent_subjects).delete()
        Semester_Plan.objects.get(program_plan=self.program_plan, 
                                  subject=subject).delete()
                                  
        uoc_removed = dependent_subjects.aggregate(tally=Sum('uoc')).get('tally', 0) or 0
        self.program_plan.uoc_tally -= uoc_removed
        self.program_plan.uoc_tally -= subject.uoc
        self.program_plan.save()