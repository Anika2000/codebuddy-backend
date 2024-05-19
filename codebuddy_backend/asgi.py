"""
ASGI config for codebuddy_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import codebuddy_app_baackend.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codebuddy_backend.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            codebuddy_app_baackend.routing.websocket_urlpatterns
        )
    ),
})
