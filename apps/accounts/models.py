"""Foydalanuvchi modellari — telefon raqami orqali kirish bilan."""
import re
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models


def validate_uzbek_phone(value):
    """O'zbekiston telefon raqami formatini tekshiradi (+998XXXXXXXXX)."""
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak"
        )


class UserManager(BaseUserManager):
    """Telefon orqali ro'yxatdan o'tkazish uchun maxsus menejer."""

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqami majburiy")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('full_name', 'Super Admin')
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """Kengaytirilgan foydalanuvchi modeli.

    Login uchun `phone` ishlatiladi. `username` o'rniga telefon raqami.
    """

    ROLE_CHOICES = [
        ('user', 'Foydalanuvchi'),
        ('operator', 'Operator'),
        ('admin', 'Administrator'),
    ]

    # username majburiy emas, lekin uniquelikni o'chiramiz
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=False,
        verbose_name='Login (ixtiyoriy)',
    )
    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[validate_uzbek_phone],
        verbose_name='Telefon raqami',
        help_text='+998XXXXXXXXX formatida',
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="To'liq ism",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Rol',
    )
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    @property
    def is_operator(self):
        return self.role == 'operator' or self.is_staff

    @property
    def is_admin_role(self):
        return self.role == 'admin' or self.is_superuser
