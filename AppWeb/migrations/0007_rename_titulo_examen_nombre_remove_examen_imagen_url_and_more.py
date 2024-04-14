# Generated by Django 5.0.3 on 2024-04-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0006_delete_examen_detallado_examen_paquete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examen',
            old_name='titulo',
            new_name='nombre',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='imagen_url',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='paquete',
        ),
        migrations.AddField(
            model_name='examen',
            name='examenes',
            field=models.ManyToManyField(related_name='paquetes', to='AppWeb.examen'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='examen',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
