from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name ='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name ='password_change_done'),
    path('registro/', views.register, name='registro'),
    path('registro-exitoso/',views.registro_done, name='registro-exitoso'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', custom_password_reset_complete, name='password_reset_complete'),
    path('agregar_al_carrito/<int:subcategoria_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mi-cuenta/editar', views.editar_perfil, name='editar_perfil'),
    path('historico/', views.ver_compras_usuario, name='historico'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('agregar_derivaciones/', views.agregar_al_carrito_derivaciones, name='agregar_derivaciones'),
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
    path('send-email/', views.send_email_view, name='send_email'),
    path('send-email-button/', views.send_email_button_view, name='send_email_button'),
    path('Nosotros', views.nosotros, name='nosotros'),
    path('terminos-condiciones/', views.terminos_condiciones_view, name='terminos_condiciones'),
    # Otros patrones de URL
]


