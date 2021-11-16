# Django Rest
from  rest_framework import serializers

# Models
from .models import ValueChange, Timer_mode_luz, Timer_mode_riego, Automatic_mode

class Control_values_serializer(serializers.ModelSerializer):
    class Meta:
        model = ValueChange
        fields = '__all__'


class Timer_mode_luz_serializer(serializers.ModelSerializer):
    class Meta:
        model = Timer_mode_luz
        fields = '__all__'


class Timer_mode_riego_serializer(serializers.ModelSerializer):
    class Meta:
        model = Timer_mode_riego
        fields = '__all__'


class Automatic_mode_serializer(serializers.ModelSerializer):
    class Meta:
        model = Automatic_mode
        fields = '__all__'


