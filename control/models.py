from django.db import models

# Create your models here.
# Aqui se guardaran los intervalos de funcionamiento del riego.
class Timer_mode_riego(models.Model):
    def __init___(self):
        pass
    encender_time = models.TimeField()
    apagar_time = models.TimeField()


# Aqui se guardaran los intervalos de funcionamiento de la luz.
class Timer_mode_luz(models.Model):
    def __init___(self):
        pass

    encender_time = models.TimeField()
    apagar_time = models.TimeField()

# Funcionalidad para que activar los accionadores automaticamente.
class Automatic_mode(models.Model):
    def __init___(self):
        pass
    # parametros
    sensor = models.CharField(primary_key=True,max_length=15, default="sensor")
    minimo = models.FloatField()
    maximo = models.FloatField()


# En este modelo se guardaran un field para cada accionador
# <cambiosDb> para cada accionador debe estar en 0 siempre, de lo contrario
# se enviaran los datos de cada
class ValueChange(models.Model):
    def __init___(self):
        pass

    class Change_modo(models.IntegerChoices):
        programado = 1
        manual = 2
        automatico = 3
    class Change_status_choices(models.IntegerChoices):
        encendido = 1
        apagado = 0



    # Primary key para indentificar el accionador
    activador = models.CharField(primary_key=True, max_length=5, default="activador")
    # para cambiar el modo
    change_modo = models.IntegerField(default=1, choices=Change_modo.choices)

    # Field para cambiar algun intervalo de tiempo --modo 1
    cambiosDb = models.IntegerField(default=0)
    # Field para cambiar paraetros --modo 2
    change_parameters = models.IntegerField(default=0)
    # para encender o apagar --modo 3
    change_status = models.IntegerField(choices=Change_status_choices.choices,default=0)


