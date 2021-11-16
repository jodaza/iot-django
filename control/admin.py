from django.contrib import admin
from .models import Timer_mode_riego, Timer_mode_luz, ValueChange, Automatic_mode
# Register your models here.

class ValueChangeAdmin(admin.ModelAdmin):
    list_display = ( 'activador','change_modo', 'cambiosDb', 'change_parameters', 'change_status')
    list_display_links = ('activador',)
    list_editable = ('change_modo', 'cambiosDb', 'change_parameters', 'change_status')

class Timer_mode_luz_admin(admin.ModelAdmin):
    """docstring for ."""
    list_display = ( 'pk','encender_time','apagar_time')
    list_display_links = ('pk',)
    list_editable = ( 'encender_time','apagar_time')

class Timer_mode_riego_admin(admin.ModelAdmin):
    """docstring for ."""
    list_display = ( 'pk','encender_time','apagar_time')
    list_display_links = ('pk',)
    list_editable = ( 'encender_time','apagar_time')

class Automatic_mode_admin(admin.ModelAdmin):
    """docstring for ."""
    list_display = ( 'sensor','minimo','maximo')
    list_display_links = ('sensor',)
    list_editable = ( 'minimo','maximo')

admin.site.register(Timer_mode_riego, Timer_mode_riego_admin)
admin.site.register(Timer_mode_luz, Timer_mode_luz_admin)
admin.site.register(ValueChange, ValueChangeAdmin)
admin.site.register(Automatic_mode, Automatic_mode_admin)