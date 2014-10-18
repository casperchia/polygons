from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import pdfcrowd

from polygons.models.Program import Program
from polygons.models.Program_Group_Member import Program_Group_Member

from comp4920.settings import PDFCROWD_USERNAME
from comp4920.settings import PDFCROWD_API_KEY

_CSE_PLANS_ID = 20382

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