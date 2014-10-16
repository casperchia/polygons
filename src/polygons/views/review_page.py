from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Subject import Subject
from polygons.models.Subject_Area import Subject_Area
from polygons.models.Career import Career
import string
import re
from polygons.forms.course_filtering import Course_Filter_Form

def review_page(request,filter=None):
    context = {}
    if request.method == 'POST':
        
        form = Course_Filter_Form(request.POST)
        
        if form.is_valid():        
            choice = form.cleaned_data['choice_field']            
            if choice == 'CAREER' :
                context = filter_career(filter,form)
            elif choice == 'SUBJECT_AREA' :
                context = filter_subject_area(filter,form)
            else :
                context = filter_letter(filter,form)
    else :
        form = Course_Filter_Form()
        filter_type = determine_filter(filter)
        if filter_type[0] == "LETTER" :
            context = filter_letter(filter,form)
        elif filter_type[0] == "CAREER" :
            context = filter_career(filter,form)
        elif filter_type[0] == "SUB_AREA" :
            context = filter_subject_area(filter,form)
        else :
            context = filter_error(filter,filter_type[1],form)
        
    return render_to_response('html/review_page.html',context, 
                              context_instance=RequestContext(request))
                              
# Determine the type of filter in the url
def determine_filter (filter):
    if filter is None :
        return ["LETTER",""]
    elif len(filter) == 1 :
        if re.match('[QXY]',filter):
            return ["ERROR","Invalid letter"]
        else :
            return ["LETTER",""]
    elif len(filter) == 2 :
        if re.match('(PG|UG|RS|NA)',filter):
            return ["CAREER",""]
        else :
            return ["ERROR","Invalid Career"]
    elif len(filter) == 4 :
        if re.match('[A-Z]{4}', filter):
            return ["SUB_AREA",""]
        else :
            return ["ERROR", "Invalid Subject Area"]
    else :
        return ["ERROR", "Invalid filter"]

# Give context error message        
def filter_error(filter,message,form):
    filter_type = 'error'
    return  {
                'error' : message,
                'form'  : form,
                'filter_type' : filter_type
            }    

def filter_letter(filter,form):
    
    if filter is None :
        subjects = Subject.objects.all()
    else :
        subjects = Subject.objects.filter(code__startswith=filter)
            
    subjects = subjects.order_by('code')    
    alphabet = list(string.ascii_uppercase)
    filter_type = 'letter'    
    return  {
                'subjects' : subjects,
                'alphabet' : alphabet,
                'form' : form,
                'filter_type' : filter_type
            }
                              
                              
def filter_subject_area(filter,form):

    if filter is None :
        sub_area = Subject_Area.objects.all()
        subjects = []
        
    else :
        area = Subject_Area.objects.get(code=filter)
        subjects = Subject.objects.filter(subject_area=area.id)
        subjects = subjects.order_by('code') 
        sub_area = []
        
    filter_type = 'subject area'
    
    return  {
                'subject_areas' : sub_area,
                'subjects' : subjects,
                'form' : form,
                'filter_type' : filter_type
            }

def filter_career(filter,form) :
    
    if filter is None :
        careers = Career.objects.all()
        subjects = []
    else :
        crr = Career.objects.get(abbreviation=filter)
        subjects = Subject.objects.filter(career=crr.id)
        subjects = subjects.order_by('code')
        careers = []
    filter_type = 'career'
    return  {
                'subjects' : subjects,
                'careers' : careers,
                'form' : form,
                'filter_type' : filter_type
            } 
