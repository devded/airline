from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_flight, name="list_flight"),
    path('new', views.create_flight, name="create_flight"),
    path('update/<int:id>', views.update_flight, name="update_flight"),
    path('delete/<int:id>', views.delete_flight, name="delete_flight"),

    path('pdf', views.render_pdf_view, name="pdf"),
    path('pdfview', views.view_pdf, name='pdf_view'),

]