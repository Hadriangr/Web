from django.urls import path,include
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
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('pago_exitoso/',views.pago_exitoso, name="pago_exitoso"),
    path('categorias/', views.ver_categorias, name='ver_categorias'),
    path('categorias/<int:categoria_id>/', views.ver_productos_por_categoria, name='ver_productos_por_categoria'),
    path('eliminar-producto/<int:item_id>/', eliminar_producto, name='eliminar_producto'),
    path('eliminar-derivacion/<int:item_id>/', eliminar_derivacion, name='eliminar_derivacion'),
    path('derivaciones', views.ver_derivaciones, name='derivaciones'),
    path('ver_diagnosticos/<int:derivacion_id>/', ver_diagnosticos, name='ver_diagnosticos'),
    path('pago_exitoso/productos_pdf/', generar_pdf_productos, name='pago_exitoso_productos_pdf'),
    path('pago_exitoso/derivaciones_pdf/', generar_pdf_derivaciones, name='pago_exitoso_derivaciones_pdf'),
    path('resumen_carrito/', views.resumen_carrito, name='resumen_carrito'),
    path('carrito/', views.carrito, name='carrito'),
]

