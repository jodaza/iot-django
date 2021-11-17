from django.shortcuts import render

# importando modelos de la app control
from .models import Timer_mode_riego, Timer_mode_luz, ValueChange, Automatic_mode

from django.http import JsonResponse

# rest
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from .serializers import Control_values_serializer, Timer_mode_luz_serializer, Timer_mode_riego_serializer, Automatic_mode_serializer

# login
class Send_all_control():
    def get(self,request):
        intervalos_riego = Timer_mode_riego.objects.all()
        intervalos_riego_segundos = []
        # Modificando los intervalos a s, y en orden:
        for intervalo in intervalos_riego:
            intervalos_riego_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
        intervalos_riego_segundos.sort()
        # Intervalos de iluminacion del modo programado
        intervalos_luz = Timer_mode_luz.objects.all()
        intervalos_luz_segundos = []
        for intervalo in intervalos_luz:
            intervalos_luz_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
        intervalos_luz_segundos.sort()
        # Parametros del modo automatico
        parametros = Automatic_mode.objects.all()
        lista_parametros = []
        for parametro in parametros:
            lista_parametros.append([parametro.minimo,parametro.maximo])
        # estado
        riego_change = ValueChange.objects.get(activador="riego")
        luz_change = ValueChange.objects.get(activador="luz")
        
        return JsonResponse([['parametros_riego',lista_parametros], ['intervalos_riego',intervalos_riego_segundos],['intervalos_luz',intervalos_luz_segundos],[riego_change.change_status,luz_change.change_status]], safe=False)


# Funcionalidad para borrar TODOS los intervalos guardados en la DB.
class Delete_times():
    # Borra intervalos RIEGO.
    def get_riego(self, request):
        Timer_mode_riego.objects.all().delete()
        return JsonResponse( list(["done!"]), safe=False)
    # Borra intervalos LUZ.
    def get_luz(self, request):
        Timer_mode_luz.objects.all().delete()
        return JsonResponse( list(["done!"]), safe=False)


# Funcionalidad para borrar TODOS los intervalos guardados en la DB.
class Delete_parameters():
    # Borra intervalos RIEGO.
    def get_riego(self, request):
        Automatic_mode.objects.all().delete()
        return JsonResponse( list(["done!"]), safe=False)

# Codigo para enviar al dispositivo los datos de las tablas de control como timer/parametros

class Send_times():
    def get(self,request,pk,change):
        # se busca el <valueChange> del activador a traves de su PK
        # va a haber solo dos PK disponibles "riego" y "luz"
        obj = ValueChange.objects.get(activador=pk)
        # ahora se cambiara el valor del <valueChange> del accionador seleccionado
        obj.cambiosDb = change
        obj.save()
        return JsonResponse(list([obj.cambiosDb]), safe=False)

class Send_parameters():
    def get(self,request,pk,change):
        # se busca el <valueChange> del activador a traves de su PK
        # va a haber solo dos PK disponibles "riego" y "luz"
        obj = ValueChange.objects.get(activador=pk)
        # ahora se cambiara el valor del <valueChange> del accionador seleccionado
        obj.change_parameters = change
        obj.save()
        return JsonResponse(list([obj.cambiosDb]), safe=False)



class curl_automatic_values(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Get Request
    def get(self, request, pk = 'temperatura'):
        values = Automatic_mode.objects.all()
        serializer =  Automatic_mode_serializer(values, many=True)
        return Response(serializer.data)
    # POST 
    def put(self, request, pk):
        if pk == 'iluminacion':
            pk = 'luz'
        sensor = Automatic_mode.objects.get(pk=pk)
        serializer = Automatic_mode_serializer(sensor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)