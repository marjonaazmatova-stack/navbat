"""Navbat tizimining asosiy modellari."""
import secrets
from django.conf import settings
from django.db import models
from django.urls import reverse


class Service(models.Model):
    """Xizmat turi (terapevt, kardiolog, hujjat olish va h.k.)."""

    name = models.CharField(
        max_length=200,
        verbose_name='Xizmat nomi',
        help_text='Masalan: Terapevt qabuli',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Tavsif',
    )
    duration_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name='Bir mijoz uchun vaqt (daqiqa)',
        help_text='Har bir slot necha daqiqa',
    )
    icon = models.CharField(
        max_length=10,
        default='🏥',
        verbose_name='Emoji belgi',
        help_text='Bitta emoji (masalan 🩺, 📋, 💊)',
    )
    color = models.CharField(
        max_length=20,
        default='blue',
        choices=[
            ('blue', "Ko'k"),
            ('emerald', 'Yashil'),
            ('amber', 'Sariq'),
            ('rose', 'Pushti'),
            ('violet', "Binafsha"),
            ('cyan', 'Moviy'),
        ],
        verbose_name='Rang',
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Xizmat'
        verbose_name_plural = 'Xizmatlar'
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}"

    def get_absolute_url(self):
        return reverse('service_detail', args=[self.id])


class Doctor(models.Model):
    """Shifokor yoki xodim."""

    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    specialty = models.CharField(max_length=200, verbose_name='Mutaxassislik')
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='doctors',
        verbose_name='Xizmat',
    )
    cabinet_number = models.CharField(
        max_length=20,
        verbose_name='Kabinet raqami',
    )
    photo = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True,
        verbose_name='Foto',
    )
    bio = models.TextField(blank=True, verbose_name='Qisqacha ma\'lumot')
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name='Tajriba (yil)',
    )
    is_active = models.BooleanField(default=True, verbose_name='Faol')

    class Meta:
        verbose_name = 'Shifokor'
        verbose_name_plural = 'Shifokorlar'
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} — {self.specialty}"

    def get_absolute_url(self):
        return reverse('doctor_detail', args=[self.id])

    @property
    def initials(self):
        """Avatar uchun bosh harflar."""
        parts = self.full_name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        return self.full_name[:2].upper()


class WorkingHours(models.Model):
    """Shifokorning haftalik ish jadvali."""

    WEEKDAY_CHOICES = [
        (0, 'Dushanba'),
        (1, 'Seshanba'),
        (2, 'Chorshanba'),
        (3, 'Payshanba'),
        (4, 'Juma'),
        (5, 'Shanba'),
        (6, 'Yakshanba'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='working_hours',
        verbose_name='Shifokor',
    )
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        verbose_name='Hafta kuni',
    )
    start_time = models.TimeField(verbose_name='Ish boshlanishi')
    end_time = models.TimeField(verbose_name='Ish tugashi')
    break_start = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Tushlik boshlanishi',
    )
    break_end = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Tushlik tugashi',
    )

    class Meta:
        verbose_name = 'Ish vaqti'
        verbose_name_plural = 'Ish vaqtlari'
        unique_together = [['doctor', 'weekday']]
        ordering = ['doctor', 'weekday']

    def __str__(self):
        return f"{self.doctor.full_name} — {self.get_weekday_display()}"


class Holiday(models.Model):
    """Dam olish va bayram kunlari."""

    date = models.DateField(unique=True, verbose_name='Sana')
    description = models.CharField(max_length=200, verbose_name='Tavsif')

    class Meta:
        verbose_name = 'Bayram kuni'
        verbose_name_plural = 'Bayram kunlari'
        ordering = ['date']

    def __str__(self):
        return f"{self.date} — {self.description}"


def generate_qr_token():
    """QR-kod uchun unique token yaratish."""
    return secrets.token_urlsafe(32)


class Appointment(models.Model):
    """Navbat (uchrashuv)."""

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('called', 'Chaqirildi'),
        ('completed', 'Yakunlandi'),
        ('cancelled', 'Bekor qilindi'),
        ('no_show', 'Kelmadi'),
    ]

    STATUS_COLORS = {
        'pending': 'blue',
        'called': 'amber',
        'completed': 'emerald',
        'cancelled': 'slate',
        'no_show': 'rose',
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Foydalanuvchi',
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Shifokor',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Xizmat',
    )
    date = models.DateField(verbose_name='Sana')
    time = models.TimeField(verbose_name='Vaqt')
    queue_number = models.PositiveIntegerField(verbose_name='Navbat raqami')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Holat',
    )
    qr_token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_qr_token,
        verbose_name='QR token',
    )
    notes = models.TextField(blank=True, verbose_name='Izohlar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Navbat'
        verbose_name_plural = 'Navbatlar'
        unique_together = [['doctor', 'date', 'time']]
        ordering = ['-date', 'time']
        indexes = [
            models.Index(fields=['date', 'doctor']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"#{self.queue_number} — {self.user.full_name} — {self.date} {self.time}"

    def get_absolute_url(self):
        return reverse('appointment_detail', args=[self.id])

    @property
    def status_color(self):
        return self.STATUS_COLORS.get(self.status, 'slate')

    @property
    def is_today(self):
        from datetime import date
        return self.date == date.today()

    @property
    def can_cancel(self):
        """2 soatdan kam vaqt qolgan bo'lsa bekor qilish mumkin emas."""
        from datetime import datetime, timedelta
        if self.status not in ('pending', 'called'):
            return False
        appointment_dt = datetime.combine(self.date, self.time)
        return appointment_dt - datetime.now() > timedelta(hours=2)
