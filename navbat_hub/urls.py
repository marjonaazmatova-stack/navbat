"""NavbatHub URL marshrutlari."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.queue import views as queue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', queue_views.home, name='home'),
    path('auth/', include('apps.accounts.urls')),
    path('', include('apps.queue.urls')),
    path('operator/', include('apps.operator.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Admin sarlavhalari
admin.site.site_header = 'NavbatHub Admin Panel'
admin.site.site_title = 'NavbatHub'
admin.site.index_title = 'Boshqaruv paneli'
