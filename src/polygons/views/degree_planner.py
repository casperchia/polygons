from django.shortcuts import render_to_response
from django.template import RequestContext
from polygons.models.Degree import Degree

def degree_planner(request):
    all_degrees = Degree.objects.all()
    context = {'degree_list': all_degrees}
    return render_to_response('html/degree_planner.html', context, 
        context_instance=RequestContext(request))
