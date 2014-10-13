from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan


class Test_Program_Plan(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject.json', 'Rule_Type.json', 'Rule.json',
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

