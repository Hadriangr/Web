from django.contrib import admin
from .models import CustomUser,Examen,SubcategoriaExamen
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Examen)
admin.site.register(SubcategoriaExamen)





