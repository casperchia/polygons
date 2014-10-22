import django.forms as forms

from polygons.models.Semester_Plan import Semester_Plan

class Remove_From_Plan_Form(forms.Form):
    
    def __init__(self, *args, **kwargs):
        subjects = kwargs.pop('subjects')
        super(Remove_From_Plan_Form, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ModelChoiceField(queryset=subjects)
    
    def save(self, request, program_plan):
        subject = self.cleaned_data['subject']
        print 'program plan id=' + program_plan.id + 'subject id=' + subject.id
        semester_plan = Semester_Plan.objects.get(program_plan_id=program_plan.id, 
                                                  subject_id=subject.id)
        semester_plan.delete()