from django.urls import path,include
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_password_reset, custom_password_reset_done, custom_password_reset_confirm, custom_password_reset_complete


urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name ='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name ='password_change_done'),
    path('examenes/', views.lista_examenes, name='Examenes'),
    path('examen/<int:examen_id>/subcategorias/', views.mostrar_subcategorias, name='mostrar_subcategorias'),
    path('registro/', SignUpView.as_view(), name='registro'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('password_reset/done/', custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', custom_password_reset_complete, name='password_reset_complete'),
    
]

