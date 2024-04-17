from django.urls import path
from .views import menu

urlpatterns = [
    path('menu/', menu, name='menu-list'),
    path('menu/<int:pk>/', menu, name='menu-detail'),
]
