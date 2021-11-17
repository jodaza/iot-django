from django.db import models

# Create your models here.

class Planta(models.Model):
    id = models.IntegerField(primary_key=True)
    especie = models.CharField(max_length=100)

class Registro(models.Model):
    descripcion = models.CharField(max_length=300)
    imagen = models.ImageField()
    fecha = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)