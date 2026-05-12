"""Navbat tizimining yordamchi funksiyalari."""
import base64
import io
from datetime import datetime, timedelta, date as date_type

import qrcode

from .models import Appointment, Holiday, WorkingHours


def get_available_slots(doctor, target_date):
    """Berilgan kunda shifokorning bo'sh vaqt slotlarini qaytaradi.

    Args:
        doctor: Doctor obyekti
        target_date: date obyekti

    Returns:
        list[time]: bo'sh slotlar ro'yxati
    """
    # O'tgan sanaga band qilish mumkin emas
    if target_date < date_type.today():
        return []

    # Bayram kuni?
    if Holiday.objects.filter(date=target_date).exists():
        return []

    # Bu kun ish kunimi?
    weekday = target_date.weekday()
    try:
        wh = WorkingHours.objects.get(doctor=doctor, weekday=weekday)
    except WorkingHours.DoesNotExist:
        return []

    duration = doctor.service.duration_minutes
    all_slots = []
    current = datetime.combine(target_date, wh.start_time)
    end = datetime.combine(target_date, wh.end_time)

    while current + timedelta(minutes=duration) <= end:
        slot_time = current.time()

        # Tushlik vaqtini o'tkazib yuborish
        if wh.break_start and wh.break_end:
            if wh.break_start <= slot_time < wh.break_end:
                current += timedelta(minutes=duration)
                continue

        all_slots.append(slot_time)
        current += timedelta(minutes=duration)

    # Band slotlarni filtrlash
    booked = set(Appointment.objects.filter(
        doctor=doctor,
        date=target_date,
        status__in=['pending', 'called'],
    ).values_list('time', flat=True))

    # Agar bugun bo'lsa, o'tib ketgan vaqtlarni filtrlash (+30 daqiqa zaxira)
    now = datetime.now()
    if target_date == date_type.today():
        cutoff = (now + timedelta(minutes=30)).time()
        all_slots = [s for s in all_slots if s > cutoff]

    return [s for s in all_slots if s not in booked]


def get_next_queue_number(doctor, target_date):
    """Berilgan kun va shifokor uchun keyingi navbat raqamini qaytaradi."""
    last_number = Appointment.objects.filter(
        doctor=doctor,
        date=target_date,
    ).count()
    return last_number + 1


def generate_qr_image(text):
    """Berilgan matn uchun QR-kod rasm yaratadi va base64 qaytaradi.

    Args:
        text: QR-kod ichidagi matn (URL yoki token)

    Returns:
        str: base64 kodlangan PNG rasm
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0f172a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def get_upcoming_dates(days=14):
    """Kelasi N kun uchun sana ro'yxatini qaytaradi.

    Returns:
        list[dict]: har biri sana, hafta kuni nomi va h.k.
    """
    weekday_short = ['Du', 'Se', 'Cho', 'Pa', 'Ju', 'Sha', 'Ya']
    month_names = [
        '', 'Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun',
        'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek'
    ]

    today = date_type.today()
    dates = []
    for i in range(days):
        d = today + timedelta(days=i)
        dates.append({
            'date': d,
            'iso': d.isoformat(),
            'day': d.day,
            'month': month_names[d.month],
            'weekday': weekday_short[d.weekday()],
            'is_weekend': d.weekday() >= 5,
            'is_today': d == today,
            'is_holiday': Holiday.objects.filter(date=d).exists(),
        })
    return dates
