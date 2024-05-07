# Generated by Django 5.0.3 on 2024-05-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0014_remove_examen_paquete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='apellido',
            field=models.CharField(max_length=100, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='comuna',
            field=models.CharField(max_length=100, verbose_name='Comuna'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electronico'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='region',
            field=models.CharField(max_length=100, verbose_name='Region'),
        ),
    ]