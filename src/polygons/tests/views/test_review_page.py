from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import Q
from polygons.models.Subject import Subject

class Test_Review_Page(TestCase):
    urls = 'comp4920.urls'
    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
                'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
                'Degree.json', 'Program.json', 'Program_Group_Member.json',
                'Subject.json', 'Rule_Type.json', 'Rule.json',
                'Program_Rule.json', 'Subject_Group_Member.json',
                'Stream.json', 'Stream_Group_Member.json', 'Stream_Rule.json']
                
    def test_status_code(self):
        url = reverse('polygons.views.review_page')
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
        url = reverse('polygons.views.review_page')

        print 'Test that the correct templates are used to render the page.'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/review_page.html')
        self.assertTemplateNotUsed(response, 'html/home.html') 
    
    def test_content(self):
        url = reverse('polygons.views.review_page')
        
        print 'Test that all subject text representations exist on the page.'
        response = self.client.get(url)
        subjects = Subject.objects.all()
        for subject in subjects:
            self.assertContains(response, str(subject.code), status_code=200)
            
        print 'Test that only subjects filter by one letter are displayed'
        response = self.client.get(url + '/W')
        for subject in Subject.objects.filter(code__startswith='W'):
            self.assertContains(response, str(subject), status_code=200)
            self.assertContains(response, subject.id, status_code=200)            
            
        print ('Testing that the page contains no other subjects.')
        for subject in Subject.objects.filter(~Q(code__startswith='W')):
            self.assertNotContains(response, str(subject), status_code=200)
            self.assertNotContains(response, subject.id, status_code=200)
            
