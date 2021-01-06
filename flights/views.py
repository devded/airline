from django.shortcuts import render, HttpResponse
from .models import Flight
# Create your views here.

def list_flight(request):
    #return HttpResponse('Hello There')
    flights = Flight.objects.all()
    #return HttpResponse(flight)
    return render(request,'flight.html', {'flights':flights})



def create_flight(request):
    pass