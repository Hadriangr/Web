from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de una URL en tu aplicación
    path('examenes-hombre/', views.examenes_hombre, name='examenes_hombre'),
    path('examenes-mujer/', views.examenes_mujer, name='examenes_mujer'),
    path('cuadro-1/', views.Mcuadro_1, name='Mcuadro_1'),
    path('cuadro-2/', views.Mcuadro_2, name='Mcuadro_2'),
    path('cuadro-3/', views.Mcuadro_3, name='Mcuadro_3'),
    path('cuadro-4/', views.Mcuadro_4, name='Mcuadro_4'),
    path('cuadro-1/', views.Hcuadro_1, name='Hcuadro_1'),
    path('cuadro-2/', views.Hcuadro_2, name='Hcuadro_2'),
    path('cuadro-3/', views.Hcuadro_3, name='Hcuadro_3'),
    path('cuadro-4/', views.Hcuadro_4, name='Hcuadro_4'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name ='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name ='password_change_done'),
    path('registro/', views.register, name='registro'),
    path('dashboard/',views.dashboard, name='dashboard'),
]
