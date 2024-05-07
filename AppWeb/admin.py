from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Derivacion)
admin.site.register(Diagnostico)





