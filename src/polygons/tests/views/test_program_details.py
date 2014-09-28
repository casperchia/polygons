from django.test import TestCase
from django.core.urlresolvers import reverse

from polygons.models.Program import Program
from polygons.utils.degree_planning import get_core_subjects
from polygons.messages import INVALID_DEGREE
        
class Test_Program_Details(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json']
    
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
        
        # ----- BEGIN INVALID DATA TESTING -----
        
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(name='Mining Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(name='Petroleum Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(code='5740')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-existent '
               'program, redirects back to the degree list page.')
        url = reverse('polygons.views.program_details', args=[2349583])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-existent '
               'program, redirects back to the degree list page.')
        url = reverse('polygons.views.program_details', args=[9999999])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
    def test_template(self):
        
        print 'Test that the correct templates are used to render the page.'
        program = Program.objects.get(name='Software Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/program_details.html')
        self.assertTemplateNotUsed(response, 'html/home.html')
        
    def test_content(self):
        
        print 'Visiting the program details page for Computer Engineering.'
        program = Program.objects.get(name='Computer Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        print ('Testing that the page contains all the core subjects for the '
               'program.')
        for subject in get_core_subjects(program):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Software Engineering.'
        program = Program.objects.get(name='Software Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        print ('Testing that the page contains all the core subjects for the '
               'program.')
        for subject in get_core_subjects(program):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Computer Science.'
        program = Program.objects.get(name='Computer Science')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        print ('Testing that the page contains all the core subjects for the '
               'program.')
        for subject in get_core_subjects(program):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Bioinformatics.'
        program = Program.objects.get(name='Bioinformatics')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        print ('Testing that the page contains all the core subjects for the '
               'program.')
        for subject in get_core_subjects(program):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        # ----- BEGIN INVALID DATA TESTING -----
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(name='Social Work')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(name='Drug Development')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(code='9065')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-existent '
               'program, redirects back to the degree list page.')
        url = reverse('polygons.views.program_details', args=[2338324])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-existent '
               'program, redirects back to the degree list page.')
        url = reverse('polygons.views.program_details', args=[777777])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)