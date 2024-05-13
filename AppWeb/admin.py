from django.contrib import admin
<<<<<<< HEAD
from .models import CustomUser,Examen,SubcategoriaExamen
=======
from .models import *
>>>>>>> origin/carrito
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
<<<<<<< HEAD
admin.site.register(Examen)
admin.site.register(SubcategoriaExamen)
=======
admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Derivacion)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
>>>>>>> origin/carrito





