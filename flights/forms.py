from django import forms
from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'duration']

        