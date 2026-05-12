"""Template'larda barcha sahifalarda mavjud bo'ladigan o'zgaruvchilar."""
from django.conf import settings


def site_info(request):
    """Sayt nomi va boshqa umumiy ma'lumotlarni qaytaradi."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'NavbatHub'),
    }
