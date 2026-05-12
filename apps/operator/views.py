"""Operator paneli view'lari."""
from datetime import date as date_type, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.queue.models import Appointment, Doctor


def is_operator(user):
    """Foydalanuvchi operator yoki adminmi tekshirish."""
    return user.is_authenticated and (user.is_operator or user.is_admin_role)


@login_required
@user_passes_test(is_operator, login_url='/auth/login/')
def dashboard(request):
    """Operator bosh sahifasi — bugungi statistika."""
    today = date_type.today()

    today_appointments = Appointment.objects.filter(date=today)

    stats = {
        'total': today_appointments.count(),
        'pending': today_appointments.filter(status='pending').count(),
        'called': today_appointments.filter(status='called').count(),
        'completed': today_appointments.filter(status='completed').count(),
        'no_show': today_appointments.filter(status='no_show').count(),
        'cancelled': today_appointments.filter(status='cancelled').count(),
    }

    doctors = Doctor.objects.filter(
        is_active=True,
        appointments__date=today,
    ).distinct()

    return render(request, 'operator/dashboard.html', {
        'stats': stats,
        'doctors': doctors,
        'today': today,
    })


@login_required
@user_passes_test(is_operator, login_url='/auth/login/')
def queue_list(request):
    """Bugungi navbatlar ro'yxati."""
    today = date_type.today()
    doctor_id = request.GET.get('doctor')

    appointments = Appointment.objects.filter(
        date=today,
    ).select_related('user', 'doctor', 'service').order_by('time')

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    doctors = Doctor.objects.filter(
        is_active=True,
        appointments__date=today,
    ).distinct()

    return render(request, 'operator/queue.html', {
        'appointments': appointments,
        'doctors': doctors,
        'selected_doctor': doctor_id,
        'today': today,
    })


@login_required
@user_passes_test(is_operator, login_url='/auth/login/')
@require_POST
def call_next(request, appointment_id):
    """Navbatni chaqirish."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Avvalgi chaqirilganini yakunlash
    Appointment.objects.filter(
        doctor=appointment.doctor,
        date=date_type.today(),
        status='called',
    ).update(status='completed')

    appointment.status = 'called'
    appointment.save()

    messages.success(request, f"Navbat #{appointment.queue_number} chaqirildi")
    return redirect('operator:queue_list')


@login_required
@user_passes_test(is_operator, login_url='/auth/login/')
@require_POST
def mark_no_show(request, appointment_id):
    """Navbatni 'kelmadi' deb belgilash."""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'no_show'
    appointment.save()
    messages.warning(request, f"Navbat #{appointment.queue_number} 'kelmadi' deb belgilandi")
    return redirect('operator:queue_list')


@login_required
@user_passes_test(is_operator, login_url='/auth/login/')
@require_POST
def mark_completed(request, appointment_id):
    """Navbatni 'yakunlandi' deb belgilash."""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'completed'
    appointment.save()
    messages.success(request, f"Navbat #{appointment.queue_number} yakunlandi")
    return redirect('operator:queue_list')


def display_board(request):
    """TV ekran uchun ochiq tablo (login talab qilmaydi).

    Doctor ID URL parametri orqali beriladi: ?doctor=1
    """
    today = date_type.today()
    doctor_id = request.GET.get('doctor')

    doctor = None
    current = None
    upcoming = []

    if doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)

        current = Appointment.objects.filter(
            doctor=doctor,
            date=today,
            status='called',
        ).select_related('user').first()

        upcoming = Appointment.objects.filter(
            doctor=doctor,
            date=today,
            status='pending',
        ).select_related('user').order_by('time')[:5]

    doctors = Doctor.objects.filter(
        is_active=True,
        appointments__date=today,
    ).distinct()

    return render(request, 'operator/display.html', {
        'doctor': doctor,
        'current': current,
        'upcoming': upcoming,
        'doctors': doctors,
        'today': today,
    })


def display_status(request, doctor_id):
    """Tablo uchun AJAX endpoint — JSON formatda joriy holat."""
    today = date_type.today()
    doctor = get_object_or_404(Doctor, id=doctor_id)

    current = Appointment.objects.filter(
        doctor=doctor,
        date=today,
        status='called',
    ).select_related('user').first()

    upcoming = list(Appointment.objects.filter(
        doctor=doctor,
        date=today,
        status='pending',
    ).order_by('time')[:5].values('queue_number', 'time'))

    return JsonResponse({
        'current': {
            'queue_number': current.queue_number if current else None,
            'cabinet': doctor.cabinet_number,
            'name': current.user.full_name if current else None,
        },
        'upcoming': [
            {
                'queue_number': u['queue_number'],
                'time': u['time'].strftime('%H:%M'),
            }
            for u in upcoming
        ],
        'timestamp': datetime.now().isoformat(),
    })
