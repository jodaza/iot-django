from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
# http
from django.http import HttpResponseRedirect, JsonResponse
# impotar los modelos de la app de get sensor values.
from get_sensor_values.models import valores_sensores, valores_sensores_hora
# importar los modelos de la app de control.
from control.models import Timer_mode_riego, Timer_mode_luz, ValueChange, Automatic_mode
"""Users views."""
from django.contrib.auth import authenticate, login, logout
# importar FORMULARIOS
from .forms import Control_mode_riego, Control_mode_luz, Control_status_riego, Control_status_luz, Add_Times_riego, Add_Times_luz, Change_graphics_form

# date time module
from datetime import datetime
my_date = datetime.today()
# AJAX API
@login_required
def last_values(request):
    ult = valores_sensores.objects.last()
    print(ult)
    def accionador_display(estado):
        if estado == 0:
            return 'Apagado'
        else:
            return 'encendido'
    valore_actuales = [ult.humedad_aire, 
                        ult.temperatura_aire,
                        ult.humedad_suelo_1,
                        ult.humedad_suelo_2,
                        ult.humedad_suelo_3,
                        ult.humedad_suelo_4,
                        ult.luz,
                        accionador_display(ult.Estado_riego),
                        accionador_display(ult.Estado_luz)]
    my_date = datetime.today()
    pp = valores_sensores_hora.objects.filter( created__year = my_date.year,
                                                created__month = my_date.month,    
                                                created__day = my_date.day,
                                                created__hour = my_date.hour)
    # tabla de los valores relevantes a la hora.
    lista = []
    for i in pp:
        lista.append([
        i.sensor,
        round((i.sumatoria/i.registros),2),
        i.minimo,
        i.maximo
    ])
    print([valore_actuales,lista])
    return JsonResponse([valore_actuales,lista], safe=False)

@login_required
def last_humemdad_values(request):
    ult = valores_sensores.objects.last()

    valore_actuales = [ult.humedad_suelo_1,
                        ult.humedad_suelo_2,
                        ult.humedad_suelo_3,
                        ult.humedad_suelo_4]

    return JsonResponse(valore_actuales, safe=False)
    
# AJAX API
@login_required
def send_intervalos_luz(request):
    luz_timers_list = Timer_mode_luz.objects.all()

    lista = []
    for intervalo in luz_timers_list:
        print(intervalo)
        lista.append([intervalo.encender_time,intervalo.apagar_time])


    return JsonResponse(list(lista), safe=False)

# INTERFACE RENDER

@login_required
def sensorviews(request):
    # llamar a los valores de la hora guardados en la base de datos.
    my_date = datetime.today()
    pp = valores_sensores_hora.objects.filter( created__year = my_date.year,
                                                created__month = my_date.month,    
                                                created__day = my_date.day,
                                                created__hour = my_date.hour)
    # tabla de los valores relevantes a la hora.
    lista = []
    for i in pp:
        lista.append({
        'name': i.sensor,
        'media': i.sumatoria/i.registros,
        'minimo': i.minimo,
        'maximo': i.maximo
    })
    # valores actuales
    ult = [valores_sensores.objects.last()]

    print((ult))
    return render(request, 'interface/sensorviews.html', {'Slist': lista, 'Lult': ult})

@login_required
def documentationviews(request):
    return render(request, 'interface/documentation.html')
@login_required
def calibrationviews(request):
    return render(request, 'interface/calibration.html')
    
@login_required
def controlviews(request):
    # Para desplegar los intervalos de tiempo
    riego_timers_list = Timer_mode_riego.objects.all()
    luz_timers_list = Timer_mode_luz.objects.all()
    automatic_list = Automatic_mode.objects.all()

    # Creamos el formulario con los datos de la instancia
    accionador_riego = ValueChange.objects.get(pk="riego")
    accionador_luz = ValueChange.objects.get(pk="luz")

    # Creamos un formulario con los datos
    mode_riego =  Control_mode_riego(instance=accionador_riego)
    mode_luz =  Control_mode_luz(instance=accionador_luz)   

    status_riego = Control_status_riego(instance=accionador_riego)
    status_luz = Control_status_luz(instance=accionador_luz)

    add_times_riego_form = Add_Times_riego()
    add_times_luz_form = Add_Times_luz()



    # Comprobamos si se ha enviado el formulario
    if 'riegomode' in request.POST:
        # Actualizamos el formulario con los datos recibidos
        mode_riego =  Control_mode_riego(request.POST,instance=accionador_riego)
        # Guardamos el formulario pero sin confirmarlo,
        # así conseguiremos una instancia para manejarla
        accionador_riego = mode_riego.save(commit=False)
        # Podemos guardarla cuando queramos
        #print(mode)
        accionador_riego.save()

    elif 'luzmode' in request.POST:
            
        mode_luz =  Control_mode_luz(request.POST,instance=accionador_luz)
        accionador_luz = mode_luz.save(commit=False)
        accionador_luz.save()

    elif 'riegostatus' in request.POST:
            
        status_riego =  Control_status_riego(request.POST,instance=accionador_riego)
        accionador_riego = status_riego.save(commit=False)
        accionador_riego.save()

    elif 'luzstatus' in request.POST:
            
        status_luz =  Control_status_luz(request.POST,instance=accionador_luz)
        accionador_luz = status_luz.save(commit=False)
        accionador_luz.save()
    elif 'addtimeriego' in request.POST:
        add_times_riego_form = Add_Times_riego(request.POST)
        newtime = add_times_riego_form.save()
    elif 'addtimeluz' in request.POST:
        add_times_luz_form = Add_Times_luz(request.POST)
        newtime = add_times_luz_form.save()
    else:
        pass

    return render(request, 'interface/control.html',{'formModeRiego':mode_riego,
    'formAddTimesRiego':add_times_riego_form,
    'formAddTimesLuz': add_times_luz_form,
    'riego_timers_list': list(riego_timers_list),
    'luz_timers_list': list(luz_timers_list),
    'automatictable':list(automatic_list),
    'formModeLuz':mode_luz,
    'formStatusRiego':status_riego,
    'formStatusLuz':status_luz,})

@login_required
def historyviews(request,  types = 'dia',sensors ='humedad_aire',years = my_date.year ,months = my_date.month ,days = my_date.day):
    # grafico diario dividido en intervalo de horas
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Change_graphics_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            tipo_sensor = form.cleaned_data['sensor']
            fecha = form.cleaned_data['fecha']
            tipo_grafico = form.cleaned_data['Tipo_de_grafico']
            #  '+tipo+'/'+sensor+'/'+ano+'/'
            return HttpResponseRedirect('/showhistory/'+tipo_grafico+'/'+tipo_sensor+'/'+str(fecha.year)+'/'+str(fecha.month)+'/'+str(fecha.day)+'/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Change_graphics_form()
    # Datos grafico

    grafico = {#'xaxis_formato':'hh:mm',
                'categories':[],
                #'xaxis_type': 'datetime',
                #'label_format': '{value:%H:%M}',

                'data': [],
                'data_rango': [],

                'titulo':'',
                'series_name':'',

                'yaxis_title':'',
                'valueSuffix':'°c',
                'yminimo':0,
                'ymax':100,
                }

    # funcion para modificar los datos enviados al grafico
    def modify_graph(tipo,sensor,graph):
        def evaluate_title(tip,sen,grap,year,month,day):
            if tip == 'dia':
                grap['titulo']  = str(day)+ "/" +  str(month)   + "/" + str(year) + " - " + ' Δ ' + sen + ' / HORA'
            elif tip == 'mes':
                grap['titulo']  = str(month)   + "/" + str(year) + " - " + ' Δ ' + sen + ' / DIA'
        # CONFIG GRAPH
        if sensor == 'humedad_aire':
            graph['valueSuffix'] = ' % '
            graph['ymax'] = 100
            graph['yaxis_title'] = 'Humedad ambiente'
            evaluate_title(tipo, 'HUMEDAD DEL AIRE', graph, years, months, days)
            graph['series_name']  = 'DTH22'
        elif sensors == 'temperatura_aire':
            graph['valueSuffix'] = ' °C '
            graph['ymax'] = 50
            graph['yaxis_title'] = 'Temperatura ambiente'
            evaluate_title(tipo, 'TEMPERATURA DEL AIRE', graph, years, months, days)
            graph['series_name']  = 'DTH22'
        elif sensors == 'humedad_suelo_1':
            graph['valueSuffix'] = ' % '
            
            graph['yminimo'] = 1000
            graph['ymax'] = 3000
            graph['yaxis_title'] = 'Humedad Suelo 1'
            evaluate_title(tipo, 'HUMEDAD DEL SUELO#1', graph , years, months, days)
            graph['series_name']  = 'sensor_humedad'
        elif sensors == 'humedad_suelo_2':
            graph['valueSuffix'] = ' % '
            graph['ymax'] = 100
            graph['yaxis_title'] = 'Humedad Suelo 2'
            evaluate_title(tipo, 'HUMEDAD DEL SUELO#1', graph, years, months, days)
            graph['series_name']  = 'sensor_humedad'
        elif sensors == 'humedad_suelo_3':
            graph['valueSuffix'] = ' % '
            graph['ymax'] = 50
            graph['yaxis_title'] = 'Humedad Suelo 3'
            evaluate_title(tipo, 'HUMEDAD DEL SUELO#1', graph , years, months, days)
            graph['series_name']  = 'sensor_humedad'
        elif sensors == 'humedad_suelo_4':
            graph['valueSuffix'] = ' % '
            graph['ymax'] = 100
            graph['yaxis_title'] = 'Humedad Suelo 4'
            evaluate_title(tipo, 'HUMEDAD DEL SUELO#1', graph , years, months, days)
            graph['series_name']  = 'sensor_humedad'
        elif sensors == 'luz':
            graph['valueSuffix'] = ' Lx '
            graph['ymax'] = 6000
            graph['yaxis_title'] = 'Humedad Suelo 4'
            evaluate_title(tipo, 'ILUMINACION', graph , years, months, days)
            graph['series_name']  = 'BH1750'
        else:
            pass

    if types == 'dia':

        lista_horas = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00',
                        '13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
        # Obteniendo la data para los distintos graficos y sensore
        # 24 valores para las 24 horas del dia
        lista = ["n","n","n","n","n","n","n","n","n","n","n","n",
                "n","n","n","n","n","n","n","n","n","n","n","n"]
                
        lista_rango = ['n','n','n','n','n','n','n','n','n','n','n','n',
                    'n','n','n','n','n','n','n','n','n','n','n','n']

        # se hace un Query de los datos registrados en el dia.
        data_graph = valores_sensores_hora.objects.filter( created__year = years,
                                                    created__month = months,    
                                                    created__day = days,
                                                    sensor = sensors)
        # se recorren los datos encontrados del dia
        for dato in data_graph:
            # en la lista se inserta en la posicion  de la hora cada dato
            lista[dato.created.hour] = dato.sumatoria/dato.registros
            lista_rango[dato.created.hour] = [dato.minimo, dato.maximo]

        modify_graph(types, sensors, grafico)


        grafico['categories']=lista_horas
        grafico['data']=lista
        grafico['data_rango']=lista_rango



    elif types == 'mes':
        lista_dias = [1,2,3,4,5,6,7,8,9,10,
                    11,12,13,14,15,16,17,18,19,20,
                    21,22,23,24,25,26,27,28,29,30,31]

        # Obteniendo la data para los distintos graficos y sensore
        # 24 valores para las 24 horas del dia
        lista = ["n","n","n","n","n","n","n","n","n","n","n","n",
                "n","n","n","n","n","n","n","n","n","n","n","n",
                "n","n","n","n","n","n","n"]
                
        lista_rango = ['n','n','n','n','n','n','n','n','n','n','n','n',
                        'n','n','n','n','n','n','n','n','n','n','n','n',
                        'n','n','n','n','n','n','n']

        # query de los datos del mes
        data_graph = valores_sensores_hora.objects.filter( created__year = years,
                                                    created__month = months,
                                                    sensor = sensors)
        
        for dia_lista in lista_dias:
            valor_medio_sum = 0
            registros = 0
            valor_minimo = 0
            valor_maximo = 0

            for dato in data_graph:

                if dato.created.day == dia_lista:
                    valor_medio_sum += dato.sumatoria
                    registros += dato.registros
                    valor_minimo += dato.minimo
                    valor_maximo += dato.maximo

            if registros != 0:
                lista[dia_lista-1] = valor_medio_sum/registros
                lista_rango[dia_lista-1] = [valor_minimo, valor_maximo]


        modify_graph(types, sensors, grafico)
        grafico['categories'] = lista_dias
        grafico['data'] = lista
        grafico['data_rango'] = lista_rango

    elif types == 'real':
        pass  
    else:
        pass 


    return render(request, 'interface/historydata.html', {'grafico_datos':grafico,'cambiar_grafico_form':Change_graphics_form},)

@login_required
def logouts(request):
    logout(request)
    return redirect('login')

class MainInterface():

    # funcion para desplegar la vista de Log In.
    def logins(self, request):
        if request.method =='POST':

            print('*' * 10)
            username = request.POST['username']
            password = request.POST['password']
            print(username, ':', password)
            print('*' * 10)

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('sensorview')
            else:
                return render(request, 'login.html', {'error': 'Invalid username and password'})

        return render(request, 'login.html')
