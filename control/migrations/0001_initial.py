# Generated by Django 3.1.4 on 2021-04-08 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automatic_mode',
            fields=[
                ('sensor', models.CharField(default='sensor', max_length=15, primary_key=True, serialize=False)),
                ('minimo', models.FloatField()),
                ('maximo', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Timer_mode_luz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encender_time', models.TimeField()),
                ('apagar_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Timer_mode_riego',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encender_time', models.TimeField()),
                ('apagar_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ValueChange',
            fields=[
                ('activador', models.CharField(default='activador', max_length=5, primary_key=True, serialize=False)),
                ('change_modo', models.IntegerField(choices=[(1, 'Programado'), (2, 'Manual'), (3, 'Automatico')], default=1)),
                ('cambiosDb', models.IntegerField(default=0)),
                ('change_parameters', models.IntegerField(default=0)),
                ('change_status', models.IntegerField(choices=[(1, 'Encendido'), (0, 'Apagado')], default=0)),
            ],
        ),
    ]
