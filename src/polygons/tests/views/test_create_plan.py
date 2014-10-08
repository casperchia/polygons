from django.test import TestCase
from django.core.urlresolvers import reverse

#from polygons.utils.PageForm import PageForm
#from polygons.models.Plan import Plan

class Test_create_plan(TestCase):
    urls = 'comp4920.urls'
#    fixtures = ['Acad_Obj_Group_Type.json', 'Acad_Obj_Group.json',
 #               'Org_Unit_Type.json', 'Org_Unit.json', 'Career.json',
  #              'Degree.json', 'Program.json', 'Program_Group_Member.json']

    def test_status_code(self):
        url = reverse('polygons.views.create_plan')

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
        url = reverse('polygons.views.create_plan')

        print 'Test that the correct templates are used to render the page.'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'html/planner.html')
        self.assertTemplateNotUsed(response, 'html/home.html')

   # def test_valid_form(self):
    #    print 'Checking the valid data.'
     #   lan = Plan.objects.create(user ='Foo')
      #  form = PageForm(data={'plan_0' : lan.user,
                                #'plan_1' : lan.pk,
        #                       })
       # self.assertTrue(form.is_valid())
        
