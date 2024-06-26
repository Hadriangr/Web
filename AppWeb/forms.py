from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms.widgets import DateInput
from django.forms.widgets import SelectDateWidget
from django.core.exceptions import ValidationError




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class CustomUserCreationForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(
        widget=SelectDateWidget(
            years=range(2024, 1899, -1)  # Rango de años para el calendario desplegable
        )
    )
    terminosCheckbox = forms.BooleanField(
        required=True,
        label='Acepto los términos y condiciones',
        error_messages={'required': 'Debe aceptar los términos y condiciones'}
    )

    email = forms.EmailField(label='Correo electrónico', max_length=254, help_text='Required. Inform a valid email address.')
    email_confirm = forms.EmailField(label='Confirmar correo electrónico')

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('nombre', 'apellido', 'email', 'email_confirm', 'region', 'comuna', 'direccion', 'telefono_contacto', 'fecha_nacimiento', 'rut', 'genero', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Asignar el email como username
        if commit:
            user.save()
        return user

    fecha_nacimiento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # Cambia el sufijo a una cadena vacía

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email_confirm = cleaned_data.get("email_confirm")

        # Verificar que ambos campos existen en cleaned_data
        if email is not None and email_confirm is not None:
            # Validar que ambos correos electrónicos sean iguales
            if email != email_confirm:
                raise forms.ValidationError(
                    _("Los correos electrónicos no coinciden."),
                    code='emails_no_coinciden',
                )
        return cleaned_data

