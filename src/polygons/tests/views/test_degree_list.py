from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.views.degree_list import CSE_PLANS_ID
from polygons.models.Program_Group_Member import Program_Group_Member
        
class Test_details_test(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json']
    
    def test_status_code(self):
        url = reverse('polygons.views.degree_list')
        
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
        url = reverse('polygons.views.degree_list')
    
        print 'Test that the correct templates are used to render the page.'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/degree_list.html')
        self.assertTemplateNotUsed(response, 'html/home.html')
        
    def test_content(self):
        url = reverse('polygons.views.degree_list')
        
        print 'Test that all CSE degree text representations exist on the page.'
        response = self.client.get(url)
        programs = [pgm.program for pgm in Program_Group_Member.objects.filter(acad_obj_group=CSE_PLANS_ID).select_related('program')]
        for program in programs:
            self.assertContains(response, str(program), status_code=200)
            
        print 'Test that all CSE degree IDs exist on the page.'
        response = self.client.get(url)
        for program in programs:
            self.assertContains(response, str(program.id), status_code=200)