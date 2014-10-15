from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program import Program
from polygons.models.Semester import Semester
from polygons.models.Subject import Subject
from polygons.models.Semester_Plan import Semester_Plan



class Test_Program_Plan(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject_Area.json', 'Subject.json', 'Rule_Type.json', 'Rule.json',
                'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json',
                'Semester.json', 'Program_Plan.json', 'Semester_Plan.json']  

    def test_status_code(self):
        print 'Starting tests for program_plan...'

        print 'Test that visiting the page produces a 202 status code.'
        plan = Program_Plan.objects.get(pk=100)
        url = reverse('polygons.views.program_plan', args=[plan.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        print 'Test that visiting the page produces a 202 status code.'
        plan = Program_Plan.objects.get(pk=101)
        url = reverse('polygons.views.program_plan', args=[plan.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + '123/')
        self.assertEqual(response.status_code, 404)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + 'abc/')
        self.assertEqual(response.status_code, 404)

    def test_template(self):
        print 'Test that the correct templates are used to render the page.'
        plan = Program_Plan.objects.get(pk=100)
        url = reverse('polygons.views.program_plan', args=[plan.id])
        response = self.client.post(url)
        self.assertTemplateUsed(response, 'html/program_plan.html')
        self.assertTemplateNotUsed(response, 'html/home.html')  

    def test_content(self):
        print 'Test that new program plan contains no subjects.'
        program = Program.objects.get(name='Computer Engineering')
        semester_2 = Semester.objects.get(name='Semester 2')
        plan = Program_Plan(program=program, uoc_tally=12, current_semester=semester_2, current_year=1)
        plan.save()
        url = reverse('polygons.views.program_plan', args=[plan.id])
        response = self.client.post(url)
        for subject in Subject.objects.all():
            self.assertNotContains(response, subject, status_code=200)

        print 'Test that added subject will display on planner page'
        subject_comp2041 = Subject.objects.get(code='COMP2041')
        semester_1 = Semester.objects.get(name='Semester 1')
        new_semester_plan = Semester_Plan(program_plan=plan, subject=subject_comp2041, semester=semester_1, year=1)
        new_semester_plan.save()
        response = self.client.post(url)
        self.assertContains(response, subject_comp2041, status_code=200)

        print 'Test that added subject will display on planner page'
        subject_comp3311 = Subject.objects.get(code='COMP3311')
        new_semester_plan2 = Semester_Plan(program_plan=plan, subject=subject_comp3311, semester=semester_1, year=1)
        new_semester_plan2.save()
        response = self.client.post(url)
        self.assertContains(response, subject_comp3311, status_code=200)

        print 'Test that removed subject will not display on planner page'
        new_semester_plan.delete()
        response = self.client.post(url)
        self.assertNotContains(response, subject_comp2041, status_code=200)
        self.assertContains(response, subject_comp3311, status_code=200)