from fpdf import FPDF, HTMLMixin
from django.template.loader import get_template, render_to_string
from django.shortcuts import HttpResponse
from django.template import Context, Template
from io import StringIO
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
import datetime
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import render, HttpResponse, redirect
from .models import Flight
from .forms import FlightForm



def list_flight(request):
    # return HttpResponse('Hello There')
    flights = Flight.objects.all()
    # return HttpResponse(flight)
    return render(request, 'flight.html', {'flights': flights})



def create_flight(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_flight')
        # return HttpResponse('Saved')

    return render(request, 'flight-form.html', {'form': form})




def update_flight(request, id):
    flight = Flight.objects.get(id=id)
    form = FlightForm(request.POST or None, instance=flight)

    if form.is_valid():
        form.save()
        return redirect('list_flight')

    return render(request, 'flight-form.html', {'form': form, 'flight': flight})




def delete_flight(request, id):
    flight = Flight.objects.get(id=id)
    flight.delete()
    return redirect('list_flight')




#Generate PDF START
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
        path = result[0]
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
    flights = Flight.objects.all()
    template_path = 'test.html'
    context = {'myvar': 'this is your template context', 'flights': flights}
   
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

#Generate PDF END