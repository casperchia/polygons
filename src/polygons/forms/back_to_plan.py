import django.forms as forms
from polygons.forms.add_course import ADD_COURSE_SESSION_KEY

class Back_To_Plan_Form(forms.Form):

    def save(self, request):
        request.session.pop(ADD_COURSE_SESSION_KEY, False)