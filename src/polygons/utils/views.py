from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import pdfcrowd

from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member
from polygons.models.Semester import Semester
from polygons.models.Semester_Plan import Semester_Plan
from polygons.models.Program_Plan import START_YEAR

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
    
    def __init__(self, year, is_last=False, is_first=False):
        self.__year = year
        self.__plan_semesters = []
        self.__is_last = is_last
        self.__is_first = is_first
        
    def __iter__(self):
        for plan_semester in self.__plan_semesters:
            yield plan_semester
        
    @property
    def year(self):
        return self.__year
    
    @property
    def is_last(self):
        return self.__is_last
    
    @property
    def is_first(self):
        return self.__is_first
    
    def add_semester(self, plan_semester):
        plan_semester.set_is_last(True)
        if self.__plan_semesters:
            self.__plan_semesters[-1].set_is_last(False)
        else:
            plan_semester.set_is_first(True)
        self.__plan_semesters.append(plan_semester)

class Program_Plan_Semester(object):
    
    def __init__(self, semester, plan_year):
        self.__semester = semester
        self.__plan_year = plan_year
        self.__subjects = []
        self.__uoc = 0
        self.__is_uoc_full = False
        self.__is_last = False
        self.__is_first = False
        
    def __iter__(self):
        for subject in self.__subjects:
            yield subject
        
    @property
    def semester(self):
        return self.__semester
    
    @property
    def is_uoc_full(self):
        return self.__is_uoc_full
    
    @property
    def uoc(self):
        return self.__uoc
    
    def set_is_last(self, is_last):
        self.__is_last = is_last
    
    @property
    def is_last(self):
        return self.__plan_year.is_last and self.__is_last
    
    def set_is_first(self, is_first):
        self.__is_first = is_first
        
    @property
    def is_first(self):
        return self.__plan_year.is_first and self.__is_first
    
    def add_subject(self, subject):
        self.__subjects.append(subject)
        self.__uoc += subject.uoc
        if self.__uoc >= MAX_SEMESTER_UOC:
            self.__is_uoc_full = True
        else:
            self.__is_uoc_full = False

def get_formatted_plan(program_plan):
    plan_years = []
    for year in xrange(START_YEAR, program_plan.current_year + 1):
        if year == program_plan.current_year:
            is_last_year = True
        else:
            is_last_year = False
            
        if year == START_YEAR:
            is_first_year = True
        else:
            is_first_year = False
            
        plan_year = Program_Plan_Year(year, is_last=is_last_year,
                                      is_first=is_first_year)
        for semester in Semester.objects.all():
            add_semester = False

            if year < program_plan.current_year:
                add_semester = True
            elif semester != Semester.objects.get(abbreviation='S2'):
                add_semester = True
            elif program_plan.current_semester == semester:
                add_semester = True
                
            if add_semester:
                plan_semester = Program_Plan_Semester(semester, plan_year)
                for semester_plan in Semester_Plan.objects.filter(program_plan=program_plan,
                                                                  semester=semester,
                                                                  year=year):
                    plan_semester.add_subject(semester_plan.subject)
                plan_year.add_semester(plan_semester)
        plan_years.append(plan_year)                                        
    return plan_years