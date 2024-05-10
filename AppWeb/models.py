from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


#Validación de rut
def validar_rut(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    rut_numeros = rut[:-1]
    verificador = rut[-1]

    try:
        int(rut_numeros)
    except ValueError:
        return False

    if len(rut_numeros) < 7:
        return False

    multiplicadores = [2, 3, 4, 5, 6, 7, 2, 3]
    rut_reverso = rut_numeros[::-1]
    suma = sum(int(digito) * multiplicador for digito, multiplicador in zip(rut_reverso, multiplicadores))
    resto = suma % 11
    digito_verificador_calculado = 11 - resto if resto != 0 else 0

    if digito_verificador_calculado == 10:
        digito_verificador_calculado = "K"
    else:
        digito_verificador_calculado = str(digito_verificador_calculado)

    if digito_verificador_calculado == verificador:
        return True
    else:
        return False


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    email = models.EmailField('Correo electronico', unique=True)
    region = models.CharField('Region', max_length=100)
    comuna = models.CharField('Comuna', max_length=100)
    direccion = models.CharField(max_length=255)
    telefono_contacto = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    rut = models.CharField(max_length=12, unique=True)
    genero = models.CharField(max_length=1, choices=(
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ))
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'direccion', 'telefono_contacto', 'fecha_nacimiento', 'rut', 'genero', 'region', 'comuna']

    # Definir nombres relacionados únicos para evitar la colisión con los campos homónimos en el modelo de usuario de Django
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if not validar_rut(self.rut):
            raise ValidationError({'rut': 'El RUT ingresado no es válido.'})

        edad_minima = 18
        edad_actual = timezone.now().date().year - self.fecha_nacimiento.year
        if edad_actual < edad_minima:
            raise ValidationError({'fecha_nacimiento': 'Debes ser mayor de 18 años para registrarte.'})

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Examen(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen_url = models.CharField(max_length=200, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('categoria', related_name='examenes', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre



class SubcategoriaExamen(models.Model):
    nombre = models.CharField(max_length=100)
    examen = models.ForeignKey(Examen, related_name='subcategorias', on_delete=models.CASCADE)
    mensaje_para_reseña = models.TextField(default='Mensaje predeterminado')

    def __str__(self):
        return self.nombre



class CarritoDeCompras(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='carrito', on_delete=models.CASCADE)
    subcategorias = models.ManyToManyField(SubcategoriaExamen)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username}'
    





