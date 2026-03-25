from django.contrib import admin
from django.urls import path, include
from core import views  # Core views ko import kiya
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pwa.urls')), 
    path('', include('core.urls')), # 'auth/' prefix hata diya
]
    # Agar aapka 'myapp' alag se hai, toh uske liye prefix de dein 
    # warna ye home page se takrayega.
    # path('myapp/', include('myapp.urls')), 


# Media aur Static files setup
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
