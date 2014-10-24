from django.template.loader import render_to_string
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.template import RequestContext

def http_error(code, request):
    template = 'html/http/%d.html'%code
        
    if code == 404:
        responder = HttpResponseNotFound
    elif code == 500:
        responder = HttpResponseServerError
        
    return responder(render_to_string(template,
                                      context_instance=RequestContext(request)))

def response_404(request, reason=""):
    return http_error(404, request)

def response_500(request, reason=""):
    return http_error(500, request)