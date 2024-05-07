from django.urls import path,include
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registro/', SignUpView.as_view(), name='registro'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', custom_password_reset_complete, name='password_reset_complete'),
    # path('agregar_al_carrito/<int:subcategoria_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    # path('ver_carrito/<int:paquete_id>/', views.ver_carrito, name='ver_carrito'),
    # path('paquetes/', views.mostrar_paquetes, name='mostrar_paquetes'),
    # path('agregar/<int:paquete_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    # path('quitar/<int:elemento_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    # path('mostrar_examenes/<int:paquete_id>/', mostrar_examenes, name='mostrar_examenes'),
    path('carrito/', views.carrito, name='carrito'),
    path('ver_carrito/', views.ver_carrito, name="ver_carrito"),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Nueva ruta para agregar al carrito
    path('pago_exitoso/',views.pago_exitoso, name="pago_exitoso"),
    path('categorias/', views.ver_categorias, name='ver_categorias'),
    path('categorias/<int:categoria_id>/', views.ver_productos_por_categoria, name='ver_productos_por_categoria'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('derivaciones', views.ver_derivaciones, name='derivaciones'),
    path('diagnostico', ver_diagnosticos, name='ver_diagnosticos'),
    
]

