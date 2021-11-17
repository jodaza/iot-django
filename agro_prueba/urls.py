from django.contrib import admin
from django.urls import path

# get sensor views
from get_sensor_values.views import  indroduce_object, introduce_calibration_value
#, prueba_api
# control app
from control.views import Delete_times, Send_times, Delete_parameters, Send_parameters, Send_all_control, curl_automatic_values
# interface app
from interface.views import MainInterface, calibrationviews, sensorviews, logouts, controlviews, historyviews, documentationviews, last_values, send_intervalos_luz,last_humemdad_values
# rest 
from rest_framework.authtoken import views


urlpatterns = [
    path('',  MainInterface().logins, name = "login"),

    path('api_generate_token/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('gets/', indroduce_object().as_view() ),
    # control app
    path('send_all/', Send_all_control().get, name="EnviarTodo"),
    # timer:
    path('delete_times_riego/', Delete_times().get_riego, name="borrarIntervalosRiego"),
    path('delete_times_luz/', Delete_times().get_luz, name="borrarIntervalosLuz"),
    path('send_times/<str:pk>/<int:change>/', Send_times().get, name="enviar"),
    # automatico:
    path('delete_parameters_riego/', Delete_parameters().get_riego),
    path('Send_parameters/<str:pk>/<int:change>/', Send_parameters().get),
    
    # interface app
    path('showsensor/', sensorviews, name ="sensorview"),
    path('showcontrol/', controlviews, name ="controlview"),
    path('showhistory/<str:types>/<str:sensors>/<str:years>/<str:months>/<str:days>/', historyviews),
    path('showhistory/', historyviews, name ="historyview"),
    path('documentation/', documentationviews, name ="documentationviews"),
    path('calibration/', calibrationviews, name ="calibrationviews"),
    # REST
    # AJAX REQUESTS
    path('send_last_values/', last_values, name ="last_values"),
    path('send_last_humemdad_values/', last_humemdad_values, name ="last_humemdad_values"),
    path('send_last_times_luz/', send_intervalos_luz, name ="last_values_luz"),

    #path('send_calibration_values/', introduce_calibration_value.as_view(), name ='calibration_values'),
    path('send_calibration_values/<int:pk>/', introduce_calibration_value.as_view(), name ='calibration_values'),
    path('curl_auto/<str:pk>', curl_automatic_values.as_view(), name = 'curl_auto'),

    # user auth
    path('login/', MainInterface().logins, name = "login"),
    path('logout/', logouts, name = "logout"),


]