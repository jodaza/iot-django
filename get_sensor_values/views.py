# impotar los modelos de la app de get sensor values.
from .models import valores_sensores, valores_sensores_hora, Calibracion_sensores_humedad
# importar los modelos de la app de control.
from control.models import Timer_mode_riego, Timer_mode_luz, ValueChange, Automatic_mode

from django.http import JsonResponse

# rest
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import serializers, status

# datetime
from datetime import datetime

from django.db.models import  F

# borrar dps
#from django.views import View

# Esta funcionalidad recibe del dispositivo los valores de los sensores y los guarda en la DB.
# Tambien, responde al dispositivo con informacion acerca de cambios en el control
from .serializers import Sensores_serializer, Calibracion_sensores_humedad_serializer

class indroduce_object(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # POST API
    def post(self, request):
            
        # Funcion para calibrar los sensores de humedad
        def calibrar_sensores_humedad(min, max, valor):
            prom = max - min
            porcentaje = valor - min 
            per = (prom - porcentaje)/prom
            return per
        # Se guardan los datos enviados desde el microControlador en un diccionario
        datos = request.data
        # Antes de ser guardados en la base de datos, se modifica su valor electronico, con los valores guardados para la calibracion en la DB
        for i in range(1,5):
            #print(i)
            #print(datos['humedad_suelo_' + str(i)])
            valores_calibracion = Calibracion_sensores_humedad.objects.get(sensor_id=i)
            #print(valores_calibracion.valor_minimo, valores_calibracion.valor_maximo)
            datos['humedad_suelo_' + str(i)] = round(calibrar_sensores_humedad(valores_calibracion.valor_minimo, valores_calibracion.valor_maximo, datos['humedad_suelo_' + str(i)]),3)
            #print(datos['humedad_suelo_' + str(i)])
            #print('___________')

        # Se guardan los datos en la tabla valores_sensores
        serializer = Sensores_serializer(data=datos)
        serializer.is_valid(raise_exception=True)
        contratista = serializer.save()
        # Datos enviados en el POST
        data = request.data
        # Codigo para agregar valores a la tabla VALORES_SENSORES_HORA
        def introduce_values_hour(sen,url):
            s = valores_sensores_hora(sensor = sen,
            sumatoria = float(url),
            minimo= float(url),
            maximo= float(url),
            registros = 1)
            s.save()
        # Funcion para modificar
        def modify_values_hour(sen, data):
            data.sumatoria = F('sumatoria') + float(sen)
            data.registros = F('registros') + 1
            if data.minimo > float(sen):
                data.minimo = float(sen)
            if data.maximo < float(sen):
                data.maximo = float(sen)
            data.save()
        # se instancia el ultimo objeto creado en la tabla
        valores_hora = valores_sensores_hora.objects.last()
        # se instancia la hora actual
        my_date = datetime.today()
        # valores_hora.created.hour  es 5 horas mas de lo que es, necesito algo para solucionar esto, no encuentro buen research

        # Si no hay valores en la tabla, o modified y created difieren en fecha/hora:
        # crear la instancia para esa hora
        if valores_hora == None or (valores_hora.created.year != my_date.year or valores_hora.created.month != my_date.month or valores_hora.created.day != my_date.day or valores_hora.created.hour != my_date.hour):
            sensores = ['humedad_aire',
            'temperatura_aire',
            'humedad_suelo_1',
            'humedad_suelo_2',
            'humedad_suelo_3',
            'humedad_suelo_4',
            'luz']
            for i in sensores:
                n = data[i]
                introduce_values_hour(i,n)
        else:
            pp = valores_sensores_hora.objects.filter( created__year = valores_hora.created.year,
                                                            created__month = valores_hora.created.month,
                                                            created__day = valores_hora.created.day,
                                                            created__hour = valores_hora.created.hour)

            for i in pp:
                modify_values_hour(data[i.sensor],i)



                

        # Se guardan los <valueChange> del riego y luz en memoria para cambiar los intervalos de tiempo.
        riego_change = ValueChange.objects.get(activador="riego")
        luz_change = ValueChange.objects.get(activador="luz")

        # para detectar cambios en el MODO de los accionadores.
        if riego_change.change_modo != int(data["modo_riego"]) or luz_change.change_modo != int(data["modo_luz"]):

            if riego_change.change_modo != int(data["modo_riego"]):
                return JsonResponse([1,riego_change.change_modo], safe=False)

            elif luz_change.change_modo != data["modo_luz"]:
                return JsonResponse([2,luz_change.change_modo], safe=False)

        # para detectar cambios en los INTERVALOS DE FUNCIONAMIENTO de los accionadores.
        elif riego_change.cambiosDb !=0 or luz_change.cambiosDb !=0:

            if riego_change.cambiosDb != 0:
                riego_change.cambiosDb = 0
                riego_change.save()

                intervalos_riego = Timer_mode_riego.objects.all()
                intervalos_riego_segundos = []
                # Modificando los intervalos a s, y en orden:
                for intervalo in intervalos_riego:
                    intervalos_riego_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
                intervalos_riego_segundos.sort()
                return JsonResponse([3 , intervalos_riego_segundos], safe=False)

            elif luz_change.cambiosDb != 0:
                luz_change.cambiosDb = 0
                luz_change.save()
                intervalos_luz = Timer_mode_luz.objects.all()
                intervalos_luz_segundos = []
                # Modificando los intervalos a s, y en orden:
                for intervalo in intervalos_luz:
                    intervalos_luz_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
                intervalos_luz_segundos.sort()
                return JsonResponse([4 , intervalos_luz_segundos], safe=False)
                #return JsonResponse([4 ,list(intervalos_luz.values())], safe=False)

        # para detectar cambios en los PARAMETROS del riego
        elif riego_change.change_parameters != 0:

            riego_change.change_parameters = 0
            riego_change.save()
            parametros = Automatic_mode.objects.all()
            lista_parametros = []
            for parametro in parametros:
                lista_parametros.append([parametro.minimo,parametro.maximo])
                print(lista_parametros)
            return JsonResponse([5,lista_parametros], safe=False)

        # para cambiar el estado de los accionadores en el MODO MANUAL
        elif  riego_change.change_modo == 2 or luz_change.change_modo == 2:

            if riego_change.change_modo == 2 and int(data["Estado_riego"]) !=  riego_change.change_status:
                return JsonResponse([6,riego_change.change_status], safe=False)

            elif luz_change.change_modo == 2 and int(data["Estado_luz"]) !=  luz_change.change_status:
                return JsonResponse([7,luz_change.change_status], safe=False)
                
            else:
                 return JsonResponse(list("0"), safe=False)

        else:
            return JsonResponse(list("0"), safe=False)

class introduce_calibration_value(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk='dont_exists_here'):
        values = Calibracion_sensores_humedad.objects.all()
        serializer =  Calibracion_sensores_humedad_serializer(values, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        print('recive request put')
        print(request.data)
        sensor = Calibracion_sensores_humedad.objects.get(pk=pk)
        print(sensor)
        serializer = Calibracion_sensores_humedad_serializer(sensor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

