# Generated by Django 3.2 on 2024-11-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParametrosSimulacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasaInfeccion', models.FloatField()),
                ('tasaRecuperacion', models.FloatField()),
                ('poblacionInicial', models.IntegerField()),
                ('infectadosInicial', models.IntegerField()),
                ('tiempoSimulacion', models.IntegerField()),
            ],
        ),
    ]
