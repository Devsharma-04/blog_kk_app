from django.contrib import admin
from django.urls import path, include
from core import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User # <-- Ye add kiya

# --- AUTO ADMIN GENERATOR (Bina Shell ke) ---
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("✅ Admin Created: User: admin, Pass: pass1234")
except:
    pass
# --------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')), 
    path('', include('core.urls')),
]

# Media aur Static files setup (Production ke liye thoda change)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)