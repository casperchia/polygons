from django.shortcuts import render_to_response
from django.template import RequestContext

from polygons.utils.PageForm import PageForm

def create_plan(request):
       form = PageForm(auto_id=True)
    if request.method == 'POST':
        form = PageForm()
        if form.is_valid():
            form.save()
    return render_to_response('html/planner.html',
                              { 'form' : form,
                              },
                              context_instance=RequestContext(request))
    


