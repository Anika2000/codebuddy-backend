# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('generate-room-id/', views.generate_room_id, name='generate-room-id')
    # Add other URL patterns as needed
]
