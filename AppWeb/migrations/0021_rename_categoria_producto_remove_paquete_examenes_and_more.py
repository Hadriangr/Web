# Generated by Django 5.0.3 on 2024-05-03 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0020_remove_elementocarrito_examenes_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categoria',
            new_name='Producto',
        ),
        migrations.RemoveField(
            model_name='paquete',
            name='examenes',
        ),
        migrations.DeleteModel(
            name='ElementoCarrito',
        ),
        migrations.DeleteModel(
            name='Examen',
        ),
        migrations.DeleteModel(
            name='Paquete',
        ),
    ]