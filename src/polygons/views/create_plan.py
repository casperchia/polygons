from django.shortcuts import render_to_response
from django.template import RequestContext

from polygons.utils.PageForm import PageForm

def create_plan(request):
    if request.method == 'POST':
        form = PageForm()
        if form.is_valid():
            new_plan = form.save()
    else:
        form = PageForm()
    return render_to_response('html/planner.html',
                              { 'form' : form,
                              },
                              context_instance=RequestContext(request))
    


