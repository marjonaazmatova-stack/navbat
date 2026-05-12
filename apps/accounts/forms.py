"""Foydalanuvchi formlari — kirish va ro'yxatdan o'tish."""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, validate_uzbek_phone


INPUT_CLASS = (
    "w-full px-4 py-3 rounded-xl border border-slate-200 "
    "focus:border-blue-500 focus:ring-2 focus:ring-blue-100 "
    "transition-all outline-none text-slate-900 placeholder:text-slate-400"
)


class RegisterForm(UserCreationForm):
    """Ro'yxatdan o'tish formasi."""

    full_name = forms.CharField(
        label="To'liq ism",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Aliyev Vali Salimovich',
        }),
    )
    phone = forms.CharField(
        label='Telefon raqami',
        max_length=13,
        validators=[validate_uzbek_phone],
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '+998901234567',
        }),
    )
    password1 = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Kamida 6 belgi',
        }),
    )
    password2 = forms.CharField(
        label='Parolni takrorlang',
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Parolni qaytadan kiriting',
        }),
    )

    class Meta:
        model = User
        fields = ('phone', 'full_name', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError(
                "Bu telefon raqami allaqachon ro'yxatdan o'tgan"
            )
        return phone


class LoginForm(forms.Form):
    """Kirish formasi."""

    phone = forms.CharField(
        label='Telefon raqami',
        max_length=13,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '+998901234567',
            'autofocus': 'autofocus',
        }),
    )
    password = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Parolingizni kiriting',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')

        if phone and password:
            user = authenticate(phone=phone, password=password)
            if user is None:
                raise ValidationError(
                    "Telefon raqami yoki parol noto'g'ri"
                )
            cleaned_data['user'] = user
        return cleaned_data
