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


