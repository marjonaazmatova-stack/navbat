"""Operator URL marshrutlari."""
from django.urls import path
from . import views

app_name = 'operator'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('queue/', views.queue_list, name='queue_list'),
    path('call/<int:appointment_id>/', views.call_next, name='call_next'),
    path('no-show/<int:appointment_id>/', views.mark_no_show, name='mark_no_show'),
    path('complete/<int:appointment_id>/', views.mark_completed, name='mark_completed'),
    path('display/', views.display_board, name='display_board'),
    path('display/api/<int:doctor_id>/', views.display_status, name='display_status'),
]
