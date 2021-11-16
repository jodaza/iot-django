from django.forms import ModelForm, TimeInput, Textarea
from django import forms

from control.models import ValueChange, Timer_mode_riego, Timer_mode_luz
from django.utils.translation import gettext_lazy as _

# CHOICES
sensor_choice = [('',''),
                ('humedad_aire', 'Humedad aire'),
                ('temperatura_aire','Temperatura'),
                ('humedad_suelo_1','Humedad suelo 1'),
                ('humedad_suelo_2','Humedad suelo 2'),
                ('humedad_suelo_3','Humedad suelo 3'),
                ('humedad_suelo_4','Humedad suelo 4'),
                     ('luz','Iluminacion'),]
graph_choice = [('',''),('mes','Mes'),('dia','Dia'),('real','Real')]

# Para cambiar el grafico
class Change_graphics_form(forms.Form):
    sensor = forms.ChoiceField(widget=forms.Select(attrs={'color':'blue'}), choices=sensor_choice )
    fecha = forms.DateField(widget=forms.SelectDateWidget())
    Tipo_de_grafico = forms.ChoiceField(widget=forms.Select(attrs={'color':'blue'}), choices=graph_choice)

# Para cambiar el MODO de los accionadores
class Control_mode_riego(ModelForm):
    class Meta:
        model = ValueChange

        fields =  ['change_modo']
        labels = { 'change_modo': ('Modo Riego'), }

class Control_mode_luz(ModelForm):
    class Meta:
        model = ValueChange

        fields =  ['change_modo']
        labels = { 'change_modo': ('Modo Iluminacion'), }


# Para cambiar el ESTADO de los accionadores
class Control_status_riego(ModelForm):
    class Meta:
        model = ValueChange

        fields =  ['change_status']
        labels = {'change_status': ('Estado Riego '),}



class Control_status_luz(ModelForm):
    class Meta:
        model = ValueChange

        fields =  ['change_status']
        labels = {'change_status': (' Estado Iluminacion '),}



class Add_Times_riego(ModelForm):
    class Meta:
        model = Timer_mode_riego

        fields =  ['encender_time','apagar_time']

        labels = { 'encender_time': ('Encender '),'apagar_time': ('Apagar '), }
   
        widgets = {
            'encender_time': TimeInput(attrs={'type': 'time'}),
            'apagar_time': TimeInput(attrs={'type': 'time','width':'122px'}),

        }   
        error_messages = {
            'encender_time': {
                'invalid': _("This writer's name is too long."),
            },
            'apagar_time': {
                'invalid': _("This writer's name is too long."),
            }, 
        }

class Add_Times_luz(ModelForm):
    class Meta:
        model = Timer_mode_luz

        fields =  ['encender_time','apagar_time']

        labels = { 'encender_time': ('Encender'), 'apagar_time': ('Apagar'),}
        widgets = {
            'encender_time': TimeInput(attrs={'type': 'time'}),
            'apagar_time': TimeInput(attrs={'type': 'time'}),

        }    
        error_messages = {
            'encender_time': {
                'invalid': _("This writer's name is too long."),
            },
            'apagar_time': {
                'invalid': _("This writer's name is too long."),
            }, 
        }

class Control_mode_automatic(ModelForm):
    class Meta:
        model = ValueChange

        fields =  ['change_modo']
        labels = { 'change_modo': ('Modo'), }
