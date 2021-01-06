from django.urls import path
from . import views

urlpatterns = [
    path('',views.list_flight,name="list_flight"),
]