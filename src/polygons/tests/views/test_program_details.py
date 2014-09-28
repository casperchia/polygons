from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program import Program
        
class Test_Program_Details(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json']
    
    def test_status_code(self):
        print 'Test that visiting the page produces a 200 status code.'
        program = Program.objects.get(name='Computer Science')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        print 'Test that visiting the page produces a 200 status code.'
        program = Program.objects.get(name='Bioinformatics')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + '123/')
        self.assertEqual(response.status_code, 404)
        
        print 'Test that a dummy url produces 404.'
        response = self.client.get(url + 'abc/')
        self.assertEqual(response.status_code, 404)
        
        print 'Test that a dummy url produces 404.'
        response = self.client.get('/degree/')
        self.assertEqual(response.status_code, 404)
        
    def test_redirection(self):
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(name='Bioinformatics')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_template(self):
        print 'Test that the correct templates are used to render the page.'
        program = Program.objects.get(name='Software Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/program_details.html')
        self.assertTemplateNotUsed(response, 'html/home.html')
        
    def test_content(self):
        pass