# Generated by Django 5.0.3 on 2024-04-28 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0012_carritodecompras'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaqueteExamen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='examen',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examenes_categoria', to='AppWeb.categoria'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='examen',
            name='paquete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examenes_paquete', to='AppWeb.paqueteexamen'),
        ),
        migrations.AddField(
            model_name='subcategoriaexamen',
            name='paquete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='AppWeb.paqueteexamen'),
        ),
    ]
