from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import pdfcrowd

from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member
from polygons.models.Semester import Semester
from polygons.models.Semester_Plan import Semester_Plan

from comp4920.settings import PDFCROWD_USERNAME
from comp4920.settings import PDFCROWD_API_KEY

_CSE_PLANS_ID = 20382
MAX_SEMESTER_UOC = 27

def get_cse_programs():
    ids = Program_Group_Member.objects.filter(acad_obj_group=_CSE_PLANS_ID).values_list('program',
                                                                                        flat=True)
    return Program.objects.filter(id__in=ids)

def render_to_pdf(template_path, context_data, file_name):
    template = get_template(template_path)
    context = Context(context_data)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s.pdf"'%file_name
    
    client = pdfcrowd.Client(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
    pdf_output = client.convertHtml(html)
    
    response.write(pdf_output)
    
    return response

class Program_Plan_Year(object):
    
    def __init__(self, year):
        self.__year = year
        self.__plan_semesters = []
        
    def __iter__(self):
        for plan_semester in self.__plan_semesters:
            yield plan_semester
        
    @property
    def year(self):
        return self.__year
    
    def add_semester(self, plan_semester):
        self.__plan_semesters.append(plan_semester)

class Program_Plan_Semester(object):
    
    def __init__(self, semester):
        self.__semester = semester
        self.__subjects = []
        self.__uoc = 0
        self.__is_uoc_full = False
        
    def __iter__(self):
        for subject in self.__subjects:
            yield subject
        
    @property
    def semester(self):
        return self.__semester
    
    @property
    def is_uoc_full(self):
        return self.__is_uoc_full
    

    def add_subject(self, subject):
        self.__subjects.append(subject)
        self.__uoc += subject.uoc
        if self.__uoc >= MAX_SEMESTER_UOC:
            self.__is_uoc_full = True
        else:
            self.__is_uoc_full = False

def get_formatted_plan(program_plan):
    plan_years = []
    for year in xrange(1, program_plan.current_year + 1):
        plan_year = Program_Plan_Year(year)
        if year < program_plan.current_year:
            for semester in Semester.objects.all():
                plan_semester = Program_Plan_Semester(semester)
                for semester_plan in Semester_Plan.objects.filter(program_plan=program_plan,
                                                                  semester=semester,
                                                                  year=year):
                    plan_semester.add_subject(semester_plan.subject)
                plan_year.add_semester(plan_semester)
            plan_years.append(plan_year)    
        else:
            for sem in xrange(1, program_plan.current_semester.id + 1):
                semester = Semester.objects.get(id=sem)
                plan_semester = Program_Plan_Semester(semester)
                for semester_plan in Semester_Plan.objects.filter(program_plan=program_plan,
                                                                  semester=semester,
                                                                  year=year):
                    plan_semester.add_subject(semester_plan.subject)
                plan_year.add_semester(plan_semester)
            plan_years.append(plan_year)                                        
    return plan_years
