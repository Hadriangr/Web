from django.urls import path,include
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name ='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name ='password_change_done'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('examenes/', views.lista_examenes, name='Examenes'),
    path('examen/<int:examen_id>/subcategorias/', views.mostrar_subcategorias, name='mostrar_subcategorias'),
    path('registro/', SignUpView.as_view(), name='registro'),
    path('cambio_clave/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('cambio_clave/hecho/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('cambio/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('cambio/hecho/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
