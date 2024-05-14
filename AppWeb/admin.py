from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Derivacion)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(CompraHistorica)





