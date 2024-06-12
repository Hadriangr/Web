from django.db import models
from django.contrib.auth.models import AbstractUser,User
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


class Derivacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre




class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)  # Campo opcional para descripción de la categoría
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen_url = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.nombre



class Item(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    derivacion = models.ForeignKey(Derivacion, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


from django.db.models import Max

class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    numero = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.numero:
            max_num = Compra.objects.aggregate(Max('numero'))['numero__max']
            self.numero = (max_num or 0) + 1
        super().save(*args, **kwargs)

    def productos_comprados(self):
        return ', '.join([item.producto.nombre for item in self.items.all()])

    def __str__(self):
        usuario_nombre = self.usuario.nombre if self.usuario else "Usuario Desconocido"
        usuario_rut = self.usuario.rut if self.usuario else "N/A"
        productos = self.productos_comprados()
        return (f"{self.numero} - {self.fecha_compra.strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{usuario_nombre} ({usuario_rut}) - Productos: {productos}")

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    costo = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        producto_nombre = self.producto.nombre if self.producto else "Producto Desconocido"
        producto_categoria = self.producto.categoria.nombre if self.producto and self.producto.categoria else "Categoría Desconocida"

        return f"{producto_categoria} - {producto_nombre} x{self.cantidad}"




# Modelo para el carrito de compras
class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def limpiar_carrito(self):
        self.itemcarrito_set.all().delete()

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

# Modelo para los ítems en el carrito
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"1 x {self.item.nombre} en el carrito de {self.carrito.usuario.username}"



