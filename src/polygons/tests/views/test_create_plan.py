from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan


class Test_create_plan(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject_Area.json', 'Subject.json', 'Rule_Type.json',
                'Rule.json', 'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json',
                'Semester.json', 'Program_Plan.json']  

    def test_status_code(self):
        
        url = reverse('polygons.views.program_details',args=[554])
        response = self.client.post(url)
        plan_count = Program_Plan.objects.count()
        plan = Program_Plan.objects.get(pk=100)
        url = reverse('polygons.views.program_plan', args=[plan.id])

        print 'Test that visiting the page produces a 200 status code.'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + '123/')
        self.assertEqual(response.status_code, 404)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + 'abc/')
        self.assertEqual(response.status_code, 404)

    def test_template(self):
        plan = Program_Plan.objects.get(pk=100)
        url = reverse('polygons.views.program_plan', args=[plan.id])

        print 'Test that the correct templates are used to render the page.'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/program_plan.html')
        self.assertTemplateNotUsed(response, 'html/home.html')

    def test_database(self):
        print 'Test that the database is storing a new program plan'
        plan_count = Program_Plan.objects.count()
        url = reverse('polygons.views.program_details',args=[554])
        response = self.client.post(url)
        new_count = Program_Plan.objects.count()
        self.assertEqual(plan_count + 1, new_count)
        
        
