"""Demo ma'lumotlarni yuklash uchun management buyrug'i.

Foydalanish:
    python manage.py seed_demo
"""
from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.queue.models import Service, Doctor, WorkingHours, Holiday

User = get_user_model()


class Command(BaseCommand):
    help = "Demo ma'lumotlarni yaratadi (xizmatlar, shifokorlar, foydalanuvchilar)"

    def handle(self, *args, **options):
        self.stdout.write("Demo ma'lumotlarni yaratish boshlandi...\n")

        # ============ Foydalanuvchilar ============
        if not User.objects.filter(phone='+998901111111').exists():
            admin = User.objects.create_superuser(
                phone='+998901111111',
                password='admin1234',
                full_name='Super Admin',
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Admin yaratildi: +998901111111 / admin1234"))
        else:
            self.stdout.write("  → Admin allaqachon mavjud")

        if not User.objects.filter(phone='+998902222222').exists():
            operator = User.objects.create_user(
                phone='+998902222222',
                password='operator1234',
                full_name='Karimova Dilnoza',
                role='operator',
                is_staff=True,
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Operator yaratildi: +998902222222 / operator1234"))
        else:
            self.stdout.write("  → Operator allaqachon mavjud")

        if not User.objects.filter(phone='+998901234567').exists():
            test_user = User.objects.create_user(
                phone='+998901234567',
                password='test1234',
                full_name='Aliyev Vali Salimovich',
                role='user',
            )
            self.stdout.write(self.style.SUCCESS("  ✓ Test foydalanuvchi: +998901234567 / test1234"))
        else:
            self.stdout.write("  → Test foydalanuvchi allaqachon mavjud")

        # ============ Xizmatlar ============
        services_data = [
            {'name': 'Terapevt qabuli', 'icon': '🩺', 'color': 'blue',
             'duration_minutes': 15,
             'description': "Umumiy shifokor ko'rigi va dastlabki tashxis"},
            {'name': 'Stomatolog', 'icon': '🦷', 'color': 'cyan',
             'duration_minutes': 30,
             'description': "Tish davolash, profilaktika va konsultatsiya"},
            {'name': 'Hujjat olish', 'icon': '📋', 'color': 'amber',
             'duration_minutes': 10,
             'description': "Tibbiy ma'lumotnoma, retsept va boshqa hujjatlarni rasmiylashtirish"},
            {'name': 'Kardiolog', 'icon': '❤️', 'color': 'rose',
             'duration_minutes': 20,
             'description': "Yurak-qon tomir kasalliklari mutaxassisi"},
            {'name': 'Pediatr', 'icon': '👶', 'color': 'emerald',
             'duration_minutes': 15,
             'description': "Bolalar shifokori, 0-14 yosh"},
            {'name': 'Laboratoriya tahlillari', 'icon': '🧪', 'color': 'violet',
             'duration_minutes': 10,
             'description': "Qon, siydik va boshqa tahlillarni topshirish"},
        ]

        services = {}
        for data in services_data:
            service, created = Service.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            services[data['name']] = service
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Xizmat: {service.icon} {service.name}"))

        # ============ Shifokorlar ============
        doctors_data = [
            {
                'full_name': "Rahmonov Bobur Akmalovich",
                'specialty': "Terapevt, oliy toifa",
                'service_name': 'Terapevt qabuli',
                'cabinet_number': "12",
                'bio': "20 yillik tajribaga ega umumiy shifokor.",
                'experience_years': 20,
            },
            {
                'full_name': "Yusupova Nargiza Olimovna",
                'specialty': "Terapevt",
                'service_name': 'Terapevt qabuli',
                'cabinet_number': "14",
                'bio': "Bemorlarga sabr va e'tibor bilan munosabatda bo'ladi.",
                'experience_years': 8,
            },
            {
                'full_name': "Karimov Sherzod Davlatovich",
                'specialty': "Stomatolog-ortoped",
                'service_name': 'Stomatolog',
                'cabinet_number': "8",
                'bio': "Zamonaviy uskunalar bilan ishlaydi. Implantatsiya va estetik stomatologiya.",
                'experience_years': 12,
            },
            {
                'full_name': "Toshpulatova Madina Erkinovna",
                'specialty': "Qabul xodimi",
                'service_name': 'Hujjat olish',
                'cabinet_number': "3",
                'bio': "Hujjatlar va ma'lumotnomalarni tez rasmiylashtiradi.",
                'experience_years': 5,
            },
            {
                'full_name': "Ismoilov Sardor Botirovich",
                'specialty': "Kardiolog, fan nomzodi",
                'service_name': 'Kardiolog',
                'cabinet_number': "20",
                'bio': "Yurak kasalliklari bo'yicha 15 yillik tajriba.",
                'experience_years': 15,
            },
            {
                'full_name': "Nazarova Gulnoza Rashidovna",
                'specialty': "Pediatr, oliy toifa",
                'service_name': 'Pediatr',
                'cabinet_number': "5",
                'bio': "Bolalar bilan ishlash bo'yicha katta tajriba.",
                'experience_years': 18,
            },
            {
                'full_name': "Sobirov Akram Halimovich",
                'specialty': "Laborant",
                'service_name': 'Laboratoriya tahlillari',
                'cabinet_number': "2",
                'bio': "Tez va aniq natija beradigan zamonaviy laboratoriya.",
                'experience_years': 10,
            },
        ]

        doctors = []
        for data in doctors_data:
            service = services[data.pop('service_name')]
            doctor, created = Doctor.objects.get_or_create(
                full_name=data['full_name'],
                defaults={**data, 'service': service},
            )
            doctors.append(doctor)
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Shifokor: {doctor.full_name}"))

        # ============ Ish vaqtlari ============
        # Du-Ju 09:00-17:00, tushlik 13:00-14:00
        # Birinchi 4 ta shifokor uchun standart jadval
        standard_schedule = [
            (0, time(9, 0),  time(17, 0), time(13, 0), time(14, 0)),
            (1, time(9, 0),  time(17, 0), time(13, 0), time(14, 0)),
            (2, time(9, 0),  time(17, 0), time(13, 0), time(14, 0)),
            (3, time(9, 0),  time(17, 0), time(13, 0), time(14, 0)),
            (4, time(9, 0),  time(16, 0), time(13, 0), time(14, 0)),
        ]
        # 5-shifokor (Madina) - shanba ham ishlaydi
        admin_schedule = standard_schedule + [
            (5, time(9, 0), time(13, 0), None, None),
        ]
        # Kardiolog - faqat 3 kun
        cardio_schedule = [
            (0, time(10, 0), time(16, 0), None, None),
            (2, time(10, 0), time(16, 0), None, None),
            (4, time(10, 0), time(16, 0), None, None),
        ]
        # Laborant - har kuni ertalab erta
        lab_schedule = [
            (0, time(7, 30), time(13, 0), None, None),
            (1, time(7, 30), time(13, 0), None, None),
            (2, time(7, 30), time(13, 0), None, None),
            (3, time(7, 30), time(13, 0), None, None),
            (4, time(7, 30), time(13, 0), None, None),
            (5, time(8, 0),  time(12, 0), None, None),
        ]

        # Har bir shifokor uchun jadval
        schedules = {
            'Rahmonov Bobur Akmalovich': standard_schedule,
            'Yusupova Nargiza Olimovna': standard_schedule,
            'Karimov Sherzod Davlatovich': standard_schedule,
            'Toshpulatova Madina Erkinovna': admin_schedule,
            'Ismoilov Sardor Botirovich': cardio_schedule,
            'Nazarova Gulnoza Rashidovna': standard_schedule,
            'Sobirov Akram Halimovich': lab_schedule,
        }

        hours_created = 0
        for doctor in doctors:
            schedule = schedules.get(doctor.full_name, standard_schedule)
            for weekday, start, end, break_s, break_e in schedule:
                _, created = WorkingHours.objects.get_or_create(
                    doctor=doctor,
                    weekday=weekday,
                    defaults={
                        'start_time': start,
                        'end_time': end,
                        'break_start': break_s,
                        'break_end': break_e,
                    },
                )
                if created:
                    hours_created += 1
        if hours_created:
            self.stdout.write(self.style.SUCCESS(f"  ✓ Ish vaqtlari yaratildi: {hours_created} ta"))

        # ============ Bayramlar ============
        current_year = date.today().year
        holidays_data = [
            (date(current_year, 1, 1), "Yangi yil"),
            (date(current_year, 1, 14), "Vatan himoyachilari kuni"),
            (date(current_year, 3, 8), "Xalqaro xotin-qizlar kuni"),
            (date(current_year, 3, 21), "Navro'z bayrami"),
            (date(current_year, 5, 9), "Xotira va qadrlash kuni"),
            (date(current_year, 9, 1), "Mustaqillik kuni"),
            (date(current_year, 10, 1), "O'qituvchilar va murabbiylar kuni"),
            (date(current_year, 12, 8), "Konstitutsiya qabul qilingan kun"),
        ]
        # Keyingi yil uchun ham
        for d, desc in holidays_data[:4]:
            holidays_data.append((date(current_year + 1, d.month, d.day), desc))

        holidays_created = 0
        for d, desc in holidays_data:
            _, created = Holiday.objects.get_or_create(
                date=d,
                defaults={'description': desc},
            )
            if created:
                holidays_created += 1
        if holidays_created:
            self.stdout.write(self.style.SUCCESS(f"  ✓ Bayramlar yaratildi: {holidays_created} ta"))

        self.stdout.write(self.style.SUCCESS("\n✅ Demo ma'lumotlar muvaffaqiyatli yaratildi!\n"))
        self.stdout.write("Test hisoblar:")
        self.stdout.write(self.style.WARNING("  Admin:    +998901111111 / admin1234"))
        self.stdout.write(self.style.WARNING("  Operator: +998902222222 / operator1234"))
        self.stdout.write(self.style.WARNING("  User:     +998901234567 / test1234"))
        self.stdout.write("")
