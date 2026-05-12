"""Queue URL marshrutlari."""
from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.services_list, name='services_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('book/<int:doctor_id>/', views.select_time, name='select_time'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/verify/<str:token>/', views.verify_appointment, name='verify_appointment'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    # AJAX (lokal, ichki API)
    path('api/slots/<int:doctor_id>/<str:date_str>/', views.api_slots, name='api_slots'),
]
