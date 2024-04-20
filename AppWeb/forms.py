from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Examen
from django.contrib.auth import authenticate



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('nombre', 'apellido', 'email', 'direccion', 'telefono_contacto', 'fecha_nacimiento', 'rut', 'genero', 'region', 'comuna')





