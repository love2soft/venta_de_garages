from django.contrib import admin

from web.models import Garage, Usuario, Categoria, Producto, Promocion
# Register your models here.

l = [Garage, Usuario, Categoria, Producto, Promocion]
for element in l:
    admin.site.register(element)
