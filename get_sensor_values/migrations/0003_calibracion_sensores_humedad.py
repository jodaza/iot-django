# Generated by Django 3.1.4 on 2021-07-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_sensor_values', '0002_auto_20210407_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calibracion_sensores_humedad',
            fields=[
                ('sensor_id', models.IntegerField(primary_key=True, serialize=False)),
                ('valor_minimo', models.IntegerField()),
                ('valor_maximo', models.IntegerField()),
            ],
        ),
    ]
