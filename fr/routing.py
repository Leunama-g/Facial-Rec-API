from django.urls import path
from .consumers import notificationConsumer

websocket_urlpatterns = [
    path('ws/notification/', notificationConsumer.as_asgi())
]