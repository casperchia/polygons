from django.core.urlresolvers import reverse
from django.db.models import Q

from polygons.models.Program import Program
from polygons.models.Subject import Subject
from polygons.messages import INVALID_DEGREE
from polygons.tests import Base_Test
        
class Test_Program_Details(Base_Test):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject_Area.json', 'Subject.json', 'Rule_Type.json',
                'Rule.json', 'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json']
    
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
        program = Program.objects.get(name='Engineering (Civil Eng w Arch)')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(name='Social Work')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        expected_url = reverse('polygons.views.degree_list')
        self.assertRedirects(response, expected_url, status_code=302,
                             target_status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'redirects back to the degree list page.')
        program = Program.objects.get(name='Music')
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
        subject_ids = [2212,1882,1880]
        for subject in Subject.objects.filter(id__in=subject_ids):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print ('Testing that the page contains no other subjects.')
        for subject in Subject.objects.filter(~Q(id__in=subject_ids)):
            self.assertNotContains(response, str(subject), status_code=200)
            self.assertNotContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Software Engineering.'
        program = Program.objects.get(name='Software Engineering')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        print 'Testing that the page contains links to the handbook entries of the courses.'
        subject_ids = [3942,3940]
        for subject in Subject.objects.filter(id__in=subject_ids):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            # TEST link to handbook page
            self.assertContains(response, subject.handbook_link, status_code=200)
            
        print ('Testing that the page contains no other subjects.')
        for subject in Subject.objects.filter(~Q(id__in=subject_ids)):
            self.assertNotContains(response, str(subject), status_code=200)
            self.assertNotContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Computer Science.'
        program = Program.objects.get(name='Computer Science')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        subject_ids = [1884,1867,1865]
        for subject in Subject.objects.filter(id__in=subject_ids):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print ('Testing that the page contains no other subjects.')
        for subject in Subject.objects.filter(~Q(id__in=subject_ids)):
            self.assertNotContains(response, str(subject), status_code=200)
            self.assertNotContains(response, subject.id, status_code=200)
            
        print 'Visiting the program details page for Bioinformatics.'
        program = Program.objects.get(name='Bioinformatics')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url)
        
        print 'Testing that the page contains a link to the handbook entry.'
        self.assertContains(response, program.handbook_link, status_code=200)
        
        print 'Testing that the page contains the program text representation.'
        self.assertContains(response, str(program), status_code=200)
        
        subject_ids = [1922,1583]
        for subject in Subject.objects.filter(id__in=subject_ids):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)
            
        print ('Testing that the page contains no other subjects.')
        for subject in Subject.objects.filter(~Q(id__in=subject_ids)):
            self.assertNotContains(response, str(subject), status_code=200)
            self.assertNotContains(response, subject.id, status_code=200)
            
        # ----- BEGIN INVALID DATA TESTING -----
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(name='Social Work')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(name='Music')
        url = reverse('polygons.views.program_details', args=[program.id])
        response = self.client.get(url, follow=True)
        self.assertContains(response, INVALID_DEGREE, status_code=200)
        
        print ('Test that trying to view program details for a non-CSE program '
               'displays an appropriate error message.')
        program = Program.objects.get(name='Engineering (Civil Eng w Arch)')
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
