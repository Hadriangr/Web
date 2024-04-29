from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate
from django.forms.widgets import SelectDateWidget




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=SelectDateWidget(
            years=range(2024, 1899, -1)  # Rango de años para el calendario desplegable
        )
    )

    class Meta:
        model = CustomUser
        fields = ('nombre', 'apellido', 'email', 'direccion', 'telefono_contacto', 'fecha_nacimiento', 'rut', 'genero', 'region', 'comuna')



