import django.forms as forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Subject import Subject
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY
from polygons.messages import INVALID_COURSE_SELECTED

class Add_To_Plan_Form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Add_To_Plan_Form, self).__init__(*args, **kwargs)

        self.fields['subject_id'] = forms.IntegerField()

    def save(self, request, program_plan, semester, year):
        subject_id = self.cleaned_data['subject_id']
        subject = Subject.objects.get(id=subject_id)
        semester_plan = Semester_Plan(program_plan=program_plan, subject=subject, semester=semester, year=year)
        try:
            semester_plan.save()
        except Exception, e:
            messages.error(request, INVALID_COURSE_SELECTED)
            request.session[ADD_COURSE_SESSION_KEY].clear()
            return HttpResponseRedirect(reverse('polygons.views.program_plan', args=[program_plan.id]))
        request.session[ADD_COURSE_SESSION_KEY].clear()
