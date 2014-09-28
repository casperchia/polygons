from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.utils.views import get_cse_programs
from polygons.models.Program import Program
        
class Test_Degree_List(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json']
    
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
        programs = get_cse_programs()
        for program in programs:
            self.assertContains(response, str(program), status_code=200)
            
        print 'Test that all CSE degree IDs exist on the page.'
        response = self.client.get(url)
        for program in programs:
            self.assertContains(response, str(program.id), status_code=200)
            
        non_cse_programs = Program.objects.all().exclude(id__in=[p.id for p in programs])
        print 'Test that non-CSE degrees don\'t appear on the page.'
        response = self.client.get(url)
        for program in non_cse_programs:
            self.assertNotContains(response, str(program), status_code=200)
