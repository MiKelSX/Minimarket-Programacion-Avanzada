# En cajero/urls.py
from django.urls import path
from . import views
from .views import finalizar_venta, reiniciar_datos

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('realizar-venta/', views.realizar_venta, name='venta'),
    path('finalizar-venta/', finalizar_venta, name='finalizar-venta'),
    path('ventas-totales/', views.ventas_totales, name='ventas_totales'),
    path('reiniciar-datos/', reiniciar_datos, name='reiniciar-datos'),
]

