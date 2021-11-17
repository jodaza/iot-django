from django.contrib import admin
from .models import Planta, Registro

class Planta_admin(admin.ModelAdmin):
    list_display = ( 'id','especie')
    list_display_links = ('id',)


class Registro_admin(admin.ModelAdmin):
    list_display = ( 'id','descripcion','imagen','fecha','created')
    list_display_links = ('id',)

admin.site.register(Planta, Planta_admin)
admin.site.register(Registro, Registro_admin)