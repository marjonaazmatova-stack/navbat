"""Navbat tizimi view'lari."""
from datetime import datetime, date as date_type, time as time_type, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Service, Doctor, Appointment, Holiday
from .utils import (
    get_available_slots,
    get_next_queue_number,
    generate_qr_image,
    get_upcoming_dates,
)


def home(request):
    """Bosh sahifa."""
    services = Service.objects.filter(is_active=True).annotate(
        doctor_count=Count('doctors', filter=Q(doctors__is_active=True))
    )[:6]

    stats = {
        'services_count': Service.objects.filter(is_active=True).count(),
        'doctors_count': Doctor.objects.filter(is_active=True).count(),
        'today_appointments': Appointment.objects.filter(
            date=date_type.today(),
            status__in=['pending', 'called', 'completed'],
        ).count(),
    }

    return render(request, 'home.html', {
        'services': services,
        'stats': stats,
    })


def services_list(request):
    """Barcha xizmatlar ro'yxati."""
    services = Service.objects.filter(is_active=True).annotate(
        doctor_count=Count('doctors', filter=Q(doctors__is_active=True))
    )
    return render(request, 'services/list.html', {'services': services})


def service_detail(request, service_id):
    """Xizmat tafsiloti va shifokorlar ro'yxati."""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    doctors = service.doctors.filter(is_active=True)
    return render(request, 'services/detail.html', {
        'service': service,
        'doctors': doctors,
    })


def doctor_detail(request, doctor_id):
    """Shifokor tafsiloti — sana tanlash sahifasi."""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    upcoming_dates = get_upcoming_dates(14)

    # Har bir sana uchun ish kunimi yoki yo'qmi belgilash
    working_weekdays = set(
        doctor.working_hours.values_list('weekday', flat=True)
    )
    for d in upcoming_dates:
        d['is_working_day'] = d['date'].weekday() in working_weekdays

    return render(request, 'doctors/detail.html', {
        'doctor': doctor,
        'upcoming_dates': upcoming_dates,
    })


@login_required
def select_time(request, doctor_id):
    """Vaqt slotini tanlash va navbat olish.

    URL: /book/<doctor_id>/?date=YYYY-MM-DD
    """
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)

    date_str = request.GET.get('date')
    if not date_str:
        return redirect('doctor_detail', doctor_id=doctor.id)

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Noto'g'ri sana formati")
        return redirect('doctor_detail', doctor_id=doctor.id)

    # Slot bandlovi (POST)
    if request.method == 'POST':
        time_str = request.POST.get('time')
        if not time_str:
            messages.error(request, "Vaqt tanlanmagan")
            return redirect(request.path + f'?date={date_str}')

        try:
            selected_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, "Noto'g'ri vaqt formati")
            return redirect(request.path + f'?date={date_str}')

        # Slot hali ham bo'shmi tekshirish
        available = get_available_slots(doctor, target_date)
        if selected_time not in available:
            messages.error(
                request,
                "Tanlangan vaqt allaqachon band qilingan. Boshqa vaqtni tanlang."
            )
            return redirect(request.path + f'?date={date_str}')

        # Foydalanuvchining shu kuni shu shifokorga band qilgani bormi?
        existing = Appointment.objects.filter(
            user=request.user,
            doctor=doctor,
            date=target_date,
            status__in=['pending', 'called'],
        ).exists()
        if existing:
            messages.warning(
                request,
                "Siz allaqachon shu shifokorga shu kunga navbat olgansiz"
            )
            return redirect('cabinet')

        # Navbat yaratish
        queue_number = get_next_queue_number(doctor, target_date)
        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            service=doctor.service,
            date=target_date,
            time=selected_time,
            queue_number=queue_number,
        )

        messages.success(
            request,
            f"Muvaffaqiyat! Sizning navbat raqamingiz: #{queue_number}"
        )
        return redirect('appointment_detail', appointment_id=appointment.id)

    # Bo'sh slotlarni olish
    available_slots = get_available_slots(doctor, target_date)

    # Slotlarni vaqt davriga ajratish (ertalab/peshindan keyin)
    morning_slots = [s for s in available_slots if s.hour < 12]
    afternoon_slots = [s for s in available_slots if 12 <= s.hour < 17]
    evening_slots = [s for s in available_slots if s.hour >= 17]

    return render(request, 'booking/select_time.html', {
        'doctor': doctor,
        'target_date': target_date,
        'morning_slots': morning_slots,
        'afternoon_slots': afternoon_slots,
        'evening_slots': evening_slots,
        'has_slots': bool(available_slots),
    })


@login_required
def appointment_detail(request, appointment_id):
    """Navbat tafsilotlari (QR-kod bilan)."""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Faqat egasi ko'ra olsin (yoki admin/operator)
    if appointment.user != request.user and not request.user.is_operator:
        raise Http404("Sahifa topilmadi")

    # QR-kod yaratish
    from django.conf import settings as dj_settings
    qr_url = request.build_absolute_uri(
        reverse('verify_appointment', args=[appointment.qr_token])
    )
    qr_image = generate_qr_image(qr_url)

    return render(request, 'booking/confirmation.html', {
        'appointment': appointment,
        'qr_image': qr_image,
    })


def verify_appointment(request, token):
    """QR-kod orqali navbatni tekshirish (operator uchun)."""
    appointment = get_object_or_404(Appointment, qr_token=token)
    return render(request, 'booking/verify.html', {
        'appointment': appointment,
    })


@login_required
def cabinet(request):
    """Shaxsiy kabinet — foydalanuvchining barcha navbatlari."""
    today = date_type.today()

    upcoming = Appointment.objects.filter(
        user=request.user,
        date__gte=today,
        status__in=['pending', 'called'],
    ).select_related('doctor', 'service').order_by('date', 'time')

    past = Appointment.objects.filter(
        user=request.user,
    ).exclude(
        id__in=upcoming.values_list('id', flat=True)
    ).select_related('doctor', 'service').order_by('-date', '-time')[:20]

    return render(request, 'cabinet/dashboard.html', {
        'upcoming': upcoming,
        'past': past,
    })


@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    """Navbatni bekor qilish."""
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        user=request.user,
    )

    if not appointment.can_cancel:
        messages.error(
            request,
            "Bu navbatni bekor qilib bo'lmaydi (2 soatdan kam vaqt qoldi)"
        )
        return redirect('cabinet')

    appointment.status = 'cancelled'
    appointment.save()

    messages.success(request, "Navbatingiz bekor qilindi")
    return redirect('cabinet')


# ============================================================
# AJAX endpointlar (lokal JS uchun, tashqi API emas)
# ============================================================

def api_slots(request, doctor_id, date_str):
    """Berilgan kun uchun bo'sh slotlarni JSON formatda qaytaradi."""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': "Noto'g'ri sana formati"}, status=400)

    slots = get_available_slots(doctor, target_date)
    return JsonResponse({
        'date': date_str,
        'slots': [s.strftime('%H:%M') for s in slots],
        'count': len(slots),
    })
