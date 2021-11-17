from django.db import models

class valores_sensores(models.Model):
    def __init___(self):
        pass

    humedad_aire = models.FloatField()
    temperatura_aire = models.FloatField()
    humedad_suelo_1 = models.FloatField()
    humedad_suelo_2 = models.FloatField()
    humedad_suelo_3 = models.FloatField()
    humedad_suelo_4 = models.FloatField()
    luz = models.FloatField()

    Estado_riego = models.IntegerField()
    Estado_luz = models.IntegerField()

    modo_riego = models.IntegerField()
    modo_luz = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

class valores_sensores_hora(models.Model):

    sensor = models.CharField(max_length=25)

    sumatoria = models.FloatField()
    minimo = models.FloatField()
    maximo = models.FloatField()

    registros = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

class Calibracion_sensores_humedad(models.Model):
    sensor_id = models.IntegerField(primary_key=True, default=100)
    valor_minimo = models.IntegerField()
    valor_maximo = models.IntegerField()

class Valores_reales_humedad(models.Model):

    sensor_id = models.IntegerField(primary_key=True)
    valor_real = models.IntegerField()

class Bolean_choises(models.Model):
    
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    choise = models.BooleanField()
