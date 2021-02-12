from django.shortcuts import render, HttpResponse, redirect
from .models import Flight
from .forms import FlightForm
# Create your views here.

def list_flight(request):
    #return HttpResponse('Hello There')
    flights = Flight.objects.all()
    #return HttpResponse(flight)
    return render(request,'flight.html', {'flights':flights})



def create_flight(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_flight')
        #return HttpResponse('Saved')
    
    return render(request, 'flight-form.html', {'form': form})


def update_flight(request,id):
    flight = Flight.objects.get(id=id)
    form = FlightForm(request.POST or None, instance=flight)

    if form.is_valid():
        form.save()
        return redirect('list_flight')

    return render(request, 'flight-form.html', {'form': form, 'flight':flight})


def delete_flight(request,id):
    flight = Flight.objects.get(id=id)
    flight.delete()
    return redirect('list_flight')


import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa 

def generate_PDF(request):
    data = {}

    template = get_template('test.html')
    html  = template.render(Context(data))

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()            
    return HttpResponse(pdf, 'application/pdf')

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

def render_pdf_view(request):
    template_path = 'test.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


from xhtml2pdf import pisa 
from io import StringIO
from django.template.loader import get_template 
from django.template import Context 
from django.template import Context, Template
def html_to_pdf_directly(request): 
     template = get_template("test.html") 
     context = Context({'pagesize':'A4'}) 
     html = template.render(context) 
     result = StringIO.StringIO() 
     pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result) 
     if not pdf.err: 
         return HttpResponse(result.getvalue(), content_type='application/pdf') 
     else: return HttpResponse('Errors')


from django.shortcuts import HttpResponse
from django.template.loader import get_template, render_to_string

from fpdf import FPDF, HTMLMixin


class HtmlPdf(FPDF, HTMLMixin):
    pass


def print_pdf(request):    
    pdf = HtmlPdf()
    pdf.add_page()
    pdf.write_html(render_to_string('test.html'))

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
    response['Content-Type'] = 'application/pdf'

    return response

