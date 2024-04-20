from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



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


class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    telefono_contacto = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    rut = models.CharField(max_length=12, unique=True)
    genero = models.CharField(max_length=1, choices=(
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ))
    region = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)

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




class SubcategoriaExamen(models.Model):  # Cambié el nombre de la clase a SubcategoriaExamen
    nombre = models.CharField(max_length=100)
    examen = models.ForeignKey(Examen, related_name='subcategorias', on_delete=models.CASCADE)  # Relacionado con Examen, no con Categoria

    def __str__(self):
        return self.nombre
    




