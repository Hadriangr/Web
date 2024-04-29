from django.contrib import admin
from .models import CustomUser,PaqueteExamen,SubcategoriaExamen
from django.contrib.admin import AdminSite


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PaqueteExamen)
admin.site.register(SubcategoriaExamen)





