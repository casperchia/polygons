from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program_Plan import Program_Plan
from polygons.forms.add_semester import New_Semester_Form


class Test_new_semester(TestCase):
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

    def test_contain(self):
        plan = Program_Plan.objects.get(pk=100)
        plan_semester = plan.current_semester
        count = Program_Plan.objects.count()
        
        form= New_Semester_Form()
        new_semester = form.save(plan)
        new_count = Program_Plan.objects.count()

        print 'Test that the new semester is being added'
        self.assertNotEqual(plan_semester, new_semester.current_semester)

        print 'Testing year remains same when adding semester 2'
        self.assertEqual(plan.current_year, new_semester.current_year)

        new_plan = Program_Plan.objects.get(pk = 101)
        new_plan_year = new_plan.current_year
        url = reverse('polygons.views.new_semester',args=[new_plan.id])
        form= New_Semester_Form()
        new_plan_semester = form.save(new_plan)

        print 'Test that the new semester is being added as semester 1'
        self.assertNotEqual(new_plan, new_plan_semester.current_semester)

        print 'Testing year increases when adding semester 1'
        self.assertEqual(new_plan_year+1, new_plan_semester.current_year)

        print 'Testing the program_plan database remains same after adding new semester'
        self.assertEqual(count, new_count)