from django.contrib import admin
from .models import CustomUser,Paquete,Examen,ElementoCarrito
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Examen)
admin.site.register(Paquete)
admin.site.register(ElementoCarrito)





