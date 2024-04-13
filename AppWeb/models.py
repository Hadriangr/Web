from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Campos adicionales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=255)
    telefono_contacto = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    rut = models.CharField(max_length=12)
    genero = models.CharField(max_length=1, choices=(
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ))
    region = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)

    # Especificar related_name para evitar conflictos de nombres
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )



class Examen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen_url = models.CharField(max_length=200)  # Almacenar la URL de la imagen
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=1.000)

    def __str__(self):
        return self.titulo
    


class Examen_detallado(models.Model):
    nombre = models.CharField(max_length=100)
    seleccionado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre