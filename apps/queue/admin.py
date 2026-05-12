"""Queue ilovasining Django Admin sozlamalari."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Service, Doctor, WorkingHours, Holiday, Appointment


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 1
    fields = ('weekday', 'start_time', 'end_time', 'break_start', 'break_end')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon_display', 'name', 'duration_minutes', 'doctor_count', 'is_active')
    list_filter = ('is_active', 'color')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)

    def icon_display(self, obj):
        return obj.icon
    icon_display.short_description = ''

    def doctor_count(self, obj):
        return obj.doctors.count()
    doctor_count.short_description = 'Shifokorlar'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty', 'service', 'cabinet_number',
                    'experience_years', 'is_active')
    list_filter = ('service', 'is_active')
    search_fields = ('full_name', 'specialty')
    list_editable = ('is_active',)
    inlines = [WorkingHoursInline]
    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('full_name', 'specialty', 'service', 'cabinet_number')
        }),
        ('Qo\'shimcha', {
            'fields': ('photo', 'bio', 'experience_years', 'is_active')
        }),
    )


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'get_weekday_display', 'start_time', 'end_time',
                    'break_start', 'break_end')
    list_filter = ('weekday', 'doctor__service')
    search_fields = ('doctor__full_name',)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'description')
    list_filter = ('date',)
    search_fields = ('description',)
    ordering = ('-date',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('queue_number', 'user_link', 'doctor', 'date', 'time',
                    'status_badge', 'created_at')
    list_filter = ('status', 'date', 'doctor__service', 'doctor')
    search_fields = ('user__full_name', 'user__phone', 'doctor__full_name')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    readonly_fields = ('qr_token', 'created_at', 'updated_at')

    fieldsets = (
        ('Navbat', {
            'fields': ('queue_number', 'status', 'date', 'time')
        }),
        ('Kim va kimga', {
            'fields': ('user', 'doctor', 'service')
        }),
        ('Qo\'shimcha', {
            'fields': ('notes', 'qr_token', 'created_at', 'updated_at')
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.full_name)
    user_link.short_description = 'Foydalanuvchi'

    def status_badge(self, obj):
        colors = {
            'pending': '#3b82f6',
            'called': '#f59e0b',
            'completed': '#10b981',
            'cancelled': '#64748b',
            'no_show': '#ef4444',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Holat'
