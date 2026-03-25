import os
from django.core.asgi import get_asgi_application

# 1. Sabse pehle settings set karo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_kk.settings')

# 2. Phir application ko initialize karo (Imports se pehle)
django_asgi_app = get_asgi_application()

# 3. Ab baaki cheezein import karo
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns 

# 4. Final application setup
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})