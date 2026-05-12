"""Autentifikatsiya view'lari."""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm


def login_view(request):
    """Foydalanuvchini tizimga kiritish."""
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.full_name}!")

            # Rolga qarab yo'naltirish
            if user.is_operator:
                return redirect('operator:dashboard')
            next_url = request.GET.get('next') or 'cabinet'
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish."""
    if request.user.is_authenticated:
        return redirect('cabinet')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            login(request, user)
            messages.success(
                request,
                "Ro'yxatdan muvaffaqiyatli o'tdingiz! Endi navbat olishingiz mumkin."
            )
            return redirect('cabinet')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """Tizimdan chiqish."""
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz")
    return redirect('home')
