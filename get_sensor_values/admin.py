from django.contrib import admin
from .models import valores_sensores, valores_sensores_hora, Calibracion_sensores_humedad, Valores_reales_humedad, Bolean_choises

# Register your models here.

class Valores_sensores_hora_admin(admin.ModelAdmin):
    list_display = ( 'pk','sensor','sumatoria', 'minimo', 'maximo', 'registros','created')
    list_display_links = ('pk',)

class Calibracion_sensores_humedad_admin(admin.ModelAdmin):
    list_display = ( 'sensor_id','valor_minimo','valor_maximo')
    list_display_links = ('sensor_id',)

class Valores_reales_humedad_admin(admin.ModelAdmin):
    list_display = ( 'sensor_id','valor_real')
    list_display_links = ('sensor_id',)
class Bolean_choises_admin(admin.ModelAdmin):
    list_display = ( 'id','description','choise')
    list_display_links = ('id',)

class valores_sensores_admin(admin.ModelAdmin):
    list_display = ( 'pk','humedad_aire',
    'temperatura_aire',
    'humedad_suelo_1',
    'humedad_suelo_2',
    'humedad_suelo_3',
    'humedad_suelo_4',
    'luz',
    'Estado_riego',
    'Estado_luz',
    'modo_riego',
    'modo_luz',
    'created')
    list_display_links = ('pk',)


admin.site.register(valores_sensores, valores_sensores_admin)

admin.site.register(Valores_reales_humedad, Valores_reales_humedad_admin)
admin.site.register(Bolean_choises, Bolean_choises_admin)

admin.site.register(Calibracion_sensores_humedad, Calibracion_sensores_humedad_admin)
admin.site.register(valores_sensores_hora, Valores_sensores_hora_admin)
