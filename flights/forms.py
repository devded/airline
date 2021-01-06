from django import forms
from django.forms import fields
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'duration']

        