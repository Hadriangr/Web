from django.urls import path,include
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_password_reset, custom_password_reset_done, custom_password_reset_confirm,custom_password_reset_complete,agregar_al_carrito
from .views import *


urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name ='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name ='password_change_done'),
    path('registro/', views.register, name='registro'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', custom_password_reset_complete, name='password_reset_complete'),
    path('agregar_al_carrito/<int:subcategoria_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('registro_test/', views.register, name='registro_test'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mi-cuenta/editar', views.editar_perfil, name='editar_perfil'),
    
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('pago_exitoso/',views.pago_exitoso, name="pago_exitoso"),
    path('categorias/', views.ver_categorias, name='ver_categorias'),
    path('categorias/<int:categoria_id>/', views.ver_productos_por_categoria, name='ver_productos_por_categoria'),
    path('eliminar-producto/<int:item_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('eliminar-derivacion/<int:item_id>/', views.eliminar_derivacion, name='eliminar_derivacion'),
    path('derivaciones', views.ver_derivaciones, name='derivaciones'),
    path('ver_diagnosticos/<int:derivacion_id>/', views.ver_diagnosticos, name='ver_diagnosticos'),
    path('resumen_carrito/', views.resumen_carrito, name='resumen_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('generar-pdf-productos/', views.generar_pdf_productos, name='generar_pdf_productos'),
    path('generar-pdf-derivaciones/', views.generar_pdf_derivaciones, name='generar_pdf_derivaciones'),
]

