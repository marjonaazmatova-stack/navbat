# 🏥 NavbatHub

> Poliklinika va davlat xizmatlari uchun onlayn navbat tizimi. Tashqi API'lar yo'q — hammasi Django ichida.

Foydalanuvchilar uydan turib navbat oladi, QR-kod va navbat raqami olishadi. Operator kutish zalida tabloda navbatlarni boshqaradi. Mijozlar tirbandlikda kutishni unutadi.

---

## ✨ Asosiy funksiyalar

- 🔐 Telefon raqami orqali ro'yxatdan o'tish va kirish (`+998XXXXXXXXX`)
- 🩺 Xizmatlar va mutaxassislarni ko'rish, izlash
- 📅 14 kungacha oldindan sana va vaqt tanlash
- 🎫 QR-kod va unique navbat raqami avtomatik generatsiya
- 👤 Shaxsiy kabinet — barcha navbatlarni boshqarish, bekor qilish
- 🖥 Operator paneli — navbatlarni chaqirish, "kelmadi"/"yakunlandi" deb belgilash
- 📺 TV ekran tablosi (auto-refresh + ovozli signal yangi chaqiriqda)
- ⚙️ Django Admin — to'liq sozlangan boshqaruv paneli
- 🌐 Mobile-friendly responsive dizayn
- 🛡 CSRF, XSS, SQL Injection himoyalari built-in

---

## 🛠 Texnologiyalar

| Qatlam | Texnologiya |
|---|---|
| Backend | Django 5.0 |
| Database | SQLite (default) yoki PostgreSQL |
| Templates | Django Templates (HTML) |
| CSS | TailwindCSS (CDN) |
| Fonts | Manrope + Plus Jakarta Sans |
| QR | qrcode + Pillow (lokal generatsiya) |
| Static | WhiteNoise |
| Server | Gunicorn |

**Tashqi API'lar:** hech qaysisi (SMS, email, to'lov, harita — hammasi lokal/o'rnatilgan).

---

## 🚀 Lokal o'rnatish

### 1. Repo'ni klonlash

```bash
git clone https://github.com/USERNAME/navbat-hub.git
cd navbat-hub
```

### 2. Virtual muhit yaratish

```bash
python3.11 -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows
```

### 3. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilari

`.env.example` faylidan nusxa olib `.env` qiling:

```bash
cp .env.example .env
```

`.env` ichidagi `SECRET_KEY` ni o'zingiznikiga almashtiring (yangi yaratish):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Ma'lumotlar bazasini tayyorlash

```bash
python manage.py migrate
python manage.py seed_demo       # Demo ma'lumotlar yuklash
```

Bu sizga uchta test hisob beradi:

| Rol | Telefon | Parol |
|---|---|---|
| Admin | `+998901111111` | `admin1234` |
| Operator | `+998902222222` | `operator1234` |
| User | `+998901234567` | `test1234` |

### 6. Serverni ishga tushirish

```bash
python manage.py runserver
```

Endi http://localhost:8000 manzilini brauzeringizda oching!

**Foydali URL'lar:**
- 🏠 Bosh sahifa: http://localhost:8000/
- 🔐 Kirish: http://localhost:8000/auth/login/
- 👨‍⚕️ Operator: http://localhost:8000/operator/
- 🛠 Admin panel: http://localhost:8000/admin/
- 📺 Tablo: http://localhost:8000/operator/display/?doctor=1

---

## 📁 Loyiha tuzilmasi

```
navbat_hub/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example, .gitignore, .dockerignore
├── Procfile, runtime.txt          # Heroku-toifa platformalar
├── railway.json                   # Railway
├── render.yaml + build.sh         # Render
├── fly.toml + Dockerfile          # Fly.io
│
├── navbat_hub/                    # Django asosiy konfiguratsiya
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│
├── apps/
│   ├── accounts/                  # Foydalanuvchilar (custom User model)
│   ├── queue/                     # Asosiy navbat tizimi
│   │   ├── models.py              # Service, Doctor, WorkingHours, Holiday, Appointment
│   │   ├── views.py
│   │   ├── utils.py               # Slot hisoblash, QR generatsiya
│   │   ├── admin.py
│   │   └── management/commands/
│   │       └── seed_demo.py       # Demo data yaratuvchi command
│   └── operator/                  # Operator paneli va TV tablo
│
├── templates/
│   ├── base.html, partials/
│   ├── home.html, accounts/, services/, doctors/
│   ├── booking/                   # Vaqt tanlash, tasdiq, verify
│   ├── cabinet/                   # Shaxsiy kabinet
│   └── operator/                  # Dashboard, queue list, TV display
│
├── static/
│   ├── css/custom.css
│   └── img/logo.svg
│
├── media/                         # Yuklangan rasmlar (shifokor fotolari)
│
└── fixtures/initial_data.json     # Muqobil demo ma'lumot manbai
```

---

## 🌐 GitHub'ga yuklash

```bash
# Git init
git init
git add .
git commit -m "Initial commit: NavbatHub"

# GitHub'da yangi repo yarating (github.com/new)
# Repo nomi: navbat-hub

# Remote qo'shish va push
git branch -M main
git remote add origin https://github.com/USERNAME/navbat-hub.git
git push -u origin main
```

---

## ☁️ Deployment qo'llanmasi

### 1️⃣ Railway (eng oson — TAVSIYA)

1. https://railway.app ga kiring, GitHub bilan ro'yxatdan o'ting
2. **"New Project"** → **"Deploy from GitHub repo"** → repo'ni tanlang
3. Railway avtomatik `Procfile` va `railway.json` ni o'qiydi
4. **Variables** bo'limida quyidagilarni qo'shing:
   ```
   SECRET_KEY=<o'z secret key'ingiz>
   DEBUG=False
   ALLOWED_HOSTS=.railway.app
   ```
5. **Settings → Networking → Generate Domain** orqali domen oling
6. Birinchi marta deploydan keyin Railway shell'ida bir martalik:
   ```bash
   python manage.py seed_demo
   ```

**Domen:** `https://navbat-hub-production-xxxx.up.railway.app`

---

### 2️⃣ Render

1. https://render.com ga kiring
2. **"New +"** → **"Web Service"** → GitHub repo'ni ulang
3. Render avtomatik `render.yaml` ni o'qiydi
4. **Environment Variables** allaqachon yaml'da, lekin tekshirib chiqing:
   - `SECRET_KEY` — random generate
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`
5. **Create Web Service** tugmasini bosing
6. `build.sh` avtomatik `seed_demo` ni ham bajaradi

**Domen:** `https://navbat-hub.onrender.com`

> ⚠️ Render bepul tarifda 15 daqiqa harakatsiz qolsa uxlab qoladi — birinchi ochilish 30 soniyaga cho'ziladi.

---

### 3️⃣ Fly.io

```bash
# 1. Fly CLI o'rnatish
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch (fly.toml ni o'qiydi)
fly launch --no-deploy

# 4. Volume yaratish (SQLite uchun, fly.toml dagi navbat_data uchun)
fly volumes create navbat_data --region fra --size 1

# 5. Secrets
fly secrets set \
  SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())") \
  DEBUG=False \
  ALLOWED_HOSTS=.fly.dev

# 6. Deploy
fly deploy
```

**Domen:** `https://navbat-hub.fly.dev`

---

### 4️⃣ PythonAnywhere (qo'lda)

1. https://pythonanywhere.com → Sign up (Bepul)
2. **Consoles → Bash**:
   ```bash
   git clone https://github.com/USERNAME/navbat-hub.git
   cd navbat-hub
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py seed_demo
   ```
3. **Web → Add a new web app** → **Manual configuration** → Python 3.11
4. **Source code:** `/home/USERNAME/navbat-hub`
5. **Virtualenv:** `/home/USERNAME/navbat-hub/venv`
6. **WSGI configuration file** ni tahrirlang:
   ```python
   import os, sys
   path = '/home/USERNAME/navbat-hub'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'navbat_hub.settings'
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
7. **Static files:**
   - URL: `/static/`
   - Directory: `/home/USERNAME/navbat-hub/staticfiles/`
8. **Reload** tugmasini bosing

---

## 🎯 Foydalanish

### Foydalanuvchi sifatida

1. Ro'yxatdan o'ting yoki test hisob bilan kiring (`+998901234567` / `test1234`)
2. **Xizmatlar** → kerakli yo'nalishni tanlang
3. Mutaxassisni tanlang → bo'sh kunni tanlang → bo'sh vaqtni tanlang
4. **"Navbatni tasdiqlash"** ni bosing
5. QR-kod va navbat raqami chiqadi → chop eting yoki telefon'da saqlang

### Operator sifatida

1. `+998902222222` / `operator1234` bilan kiring
2. **Operator** sahifasiga o'ting (avto-yo'naltirish)
3. **Navbatlar ro'yxati** da bemorlarni chaqiring (Chaqirish / Kelmadi / Yakunlash)
4. Kutish zalida **Tablo** sahifasini ochiq qoldiring (har 5 sek auto-refresh)

### Admin sifatida

`+998901111111` / `admin1234` bilan `/admin/` ga kiring va boshqaring:
- Xizmatlar va shifokorlar
- Ish vaqtlari va bayram kunlari
- Barcha navbatlar
- Foydalanuvchilar

---

## 🔒 Xavfsizlik

- ✅ CSRF himoyasi barcha POST formlarida
- ✅ XSS — Django templates avtomatik escape
- ✅ SQL Injection — Django ORM
- ✅ Parol hashing — PBKDF2 (Django standart)
- ✅ HTTPS production'da (Railway/Render/Fly avto-SSL)
- ✅ SECRET_KEY environment'da
- ✅ `DEBUG=False` production'da
- ✅ Telefon format validatsiyasi
- ✅ Permission check'lar har bir view'da

---

## 🐛 Muammolarni bartaraf qilish

**Static fayllar ko'rinmayapti (production)?**
```bash
python manage.py collectstatic --noinput
```

**Migration xatolari?**
```bash
python manage.py migrate --run-syncdb
```

**Demo ma'lumot qayta yuklamoqchimisiz?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_demo
```

**Telefon format xato?** Format aniq: `+998` + 9 ta raqam, masalan: `+998901234567`

---

## 📊 Bonuslarni qanday qo'shish mumkin

Loyiha rivojlantirish uchun ochiq qoldirildi:
- 🌓 Dark mode (Tailwind class toggle)
- 🌍 i18n (UZ/RU/EN — `LANGUAGES` allaqachon sozlangan)
- 📊 Admin uchun Chart.js bilan statistika
- 🔔 PWA (offline ishlash)
- 🤖 Telegram bot eslatma (foydalanuvchi botga yozadi, bot polling — tashqi API emas)

---

## 📄 Litsenziya

MIT License. Erkin foydalaning, o'zgartiring, tarqating.

---

## 🤝 Muallif

Django + Tailwind asosida yaratilgan. Savol va takliflar uchun GitHub Issues orqali murojaat qiling.

**Muvaffaqiyatlar! 🚀**
