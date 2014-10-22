from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan


class Test_New_Semester(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject_Area.json', 'Subject.json', 'Rule_Type.json',
                'Rule.json', 'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json',
                'Semester.json', 'Program_Plan.json']  

    def test_status_code(self):
        url = reverse('polygons.views.new_semester',args=[100])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + '123/')
        self.assertEqual(response.status_code, 404)

        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + 'abc/')
        self.assertEqual(response.status_code, 404)

    def test_database(self):
        count = Program_Plan.objects.count()
        plan = Program_Plan.objects.get(pk=100)
        plan_semester = plan.current_semester
       
        url = reverse('polygons.views.new_semester', args=[100]) 
        response = self.client.post(url)
        new_semester = Program_Plan.objects.get(pk=100)
        new_count = Program_Plan.objects.count()
       
        print 'Test that the new semester is being added'
        self.assertNotEqual(plan_semester, new_semester.current_semester)

        print 'Testing year remains same when adding semester 2'
        self.assertEqual(plan.current_year, new_semester.current_year)

        print 'Testing the program_plan database remains same after adding new semester'
        self.assertEqual(count, new_count)

        new_plan = Program_Plan.objects.get(pk = 101)
        new_plan_year = new_plan.current_year
        url = reverse('polygons.views.new_semester',args=[new_plan.id])
        response = self.client.post(url)
        new_plan_semester = Program_Plan.objects.get(pk=101)

        print 'Test that the new semester is being added as semester 1'
        self.assertNotEqual(new_plan.current_semester, new_plan_semester.current_semester)

        print 'Testing year increases when adding semester 1'
        self.assertEqual(new_plan_year+1, new_plan_semester.current_year)

        