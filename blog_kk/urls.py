from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.views.static import serve # <-- Ye line static serving ke liye zaroori hai
import re

# --- AUTO ADMIN GENERATOR ---
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("✅ Admin Created: User: admin, Pass: pass1234")
except Exception as e:
    print(f"⚠️ Admin creation skipped: {e}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')), 
    path('', include('core.urls')),
]

# Media aur Static files serving logic (Render/Production ke liye)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # PRODUCTION MEIN STATIC/MEDIA FILES KA JUGAD
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]