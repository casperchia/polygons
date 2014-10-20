from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.messages import PROGRAM_PLAN_DELETED
from polygons.messages import INVALID_PROGRAM_PLAN
from polygons.models.Program_Plan import Program_Plan
from polygons.models.Semester_Plan import Semester_Plan

class Test_Delete_Program_Plan(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject_Area.json', 'Subject.json', 'Rule_Type.json', 'Rule.json',
                'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json',
                'Semester.json', 'Program_Plan.json', 'Semester_Plan.json']  

    def test_redirection(self):
        print 'Test that valid post data redirects to the home page.'
        url = reverse('polygons.views.delete_program_plan', args=[100])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('polygons.views.index'),
                             status_code=302, target_status_code=200)
        
        print 'Test that invalid post data redirects to the home page.'
        url = reverse('polygons.views.delete_program_plan', args=[323245])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('polygons.views.index'),
                             status_code=302, target_status_code=200)

    def test_content(self):
        print 'Test that valid post data displays success message.'
        url = reverse('polygons.views.delete_program_plan', args=[101])
        response = self.client.post(url, follow=True)
        self.assertContains(response, PROGRAM_PLAN_DELETED, status_code=200)
        self.assertNotContains(response, INVALID_PROGRAM_PLAN, status_code=200)
        
        print 'Test that invalid post data displays error message.'
        url = reverse('polygons.views.delete_program_plan', args=[345235])
        response = self.client.post(url, follow=True)
        self.assertNotContains(response, PROGRAM_PLAN_DELETED, status_code=200)
        self.assertContains(response, INVALID_PROGRAM_PLAN, status_code=200)
        
        print 'Test that invalid post data displays error message.'
        url = reverse('polygons.views.delete_program_plan', args=[0])
        response = self.client.post(url, follow=True)
        self.assertNotContains(response, PROGRAM_PLAN_DELETED, status_code=200)
        self.assertContains(response, INVALID_PROGRAM_PLAN, status_code=200)
            
    def test_database(self):
        print 'Counting the number of program and semester plans in the DB.'
        num_program_plans = Program_Plan.objects.count()
        num_semester_plans = Semester_Plan.objects.count()
        
        print 'Trying to delete a non existent program plan'
        url = reverse('polygons.views.delete_program_plan', args=[352354])
        self.client.post(url)
        
        print 'Testing that the program plan count has remained the same.'
        self.assertEqual(Program_Plan.objects.count(), num_program_plans)
        
        print 'Testing that the semester plan count has remained the same.'
        self.assertEqual(Semester_Plan.objects.count(), num_semester_plans)
        
        print 'Counting the number of program and semester plans in the DB.'
        num_program_plans = Program_Plan.objects.count()
        num_semester_plans = Semester_Plan.objects.count()
        
        print 'Deleting program plan with ID 100.'
        url = reverse('polygons.views.delete_program_plan', args=[100])
        self.client.post(url)
        
        print 'Testing that there are now less program plans in the DB.'
        self.assertLess(Program_Plan.objects.count(), num_program_plans)
        
        print 'Testing that there are now less semester plans in the DB.'
        self.assertLess(Semester_Plan.objects.count(), num_semester_plans)
        
        print 'Counting the number of program and semester plans in the DB.'
        num_program_plans = Program_Plan.objects.count()
        num_semester_plans = Semester_Plan.objects.count()
        
        print 'Trying to delete program plan with ID 100.'
        url = reverse('polygons.views.delete_program_plan', args=[100])
        self.client.post(url)
        
        print 'Testing that the program plan count has remained the same.'
        self.assertEqual(Program_Plan.objects.count(), num_program_plans)
        
        print 'Testing that the semester plan count has remained the same.'
        self.assertEqual(Semester_Plan.objects.count(), num_semester_plans)
        
        print 'Counting the number of program and semester plans in the DB.'
        num_program_plans = Program_Plan.objects.count()
        num_semester_plans = Semester_Plan.objects.count()
        
        print 'Deleting program plan with ID 101.'
        url = reverse('polygons.views.delete_program_plan', args=[101])
        self.client.post(url)
        
        print 'Testing that there are now less program plans in the DB.'
        self.assertLess(Program_Plan.objects.count(), num_program_plans)
        
        print 'Testing that the semester plan count has remained the same.'
        self.assertEqual(Semester_Plan.objects.count(), num_semester_plans)