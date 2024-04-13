from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Examen_detallado
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    rut_sin_dv = rut[:-1]
    dv = rut[-1]
    suma = 0
    multiplo = 2
    for digito in reversed(rut_sin_dv):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2
    dv_calculado = 11 - (suma % 11)
    if dv_calculado == 10:
        dv_calculado = 'K'
    elif dv_calculado == 11:
        dv_calculado = '0'
    if str(dv_calculado) == dv:
        return rut
    else:
        raise forms.ValidationError(_('RUT inválido.'))




class CustomUserCreationForm(UserCreationForm):
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    email = forms.EmailField(label="Email")
    direccion = forms.CharField(label="Dirección", max_length=255)
    telefono_contacto = forms.CharField(label="Teléfono de Contacto", max_length=20)
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        help_text=_("Formato: AAAA-MM-DD")
    )
    rut = forms.CharField(
        label="RUT",
        max_length=12,
        help_text=_("Formato: 12345678-9"),
        widget=forms.TextInput(attrs={'placeholder': '12345678-9'})
    )
    genero = forms.ChoiceField(
        label="Género",
        choices=GENERO_CHOICES
    )
    region = forms.CharField(label="Región", max_length=100)
    comuna = forms.CharField(label="Comuna", max_length=100)
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_("La contraseña debe contener al menos 8 caracteres."),
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Ingrese la misma contraseña para verificación."),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Quita los paréntesis después de CustomUser
        fields = ('email', 'password1', 'password2', 'nombre', 'apellido', 'direccion', 'telefono_contacto', 'fecha_nacimiento', 'rut', 'genero', 'region', 'comuna')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Correo Electrónico'  # Cambiar la etiqueta del campo de correo electrónico
        self.fields['email'].help_text = 'Se utilizará como nombre de usuario para iniciar sesión.'

    def clean_username(self):
        username = self.cleaned_data['email']
        if CustomUser.objects.filter(username=username).exists():  # Quita los paréntesis después de CustomUser
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user
    

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen_detallado
        fields = ['seleccionado']
        widgets = {'seleccionado': forms.CheckboxInput()}
        
