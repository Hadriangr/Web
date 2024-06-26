# Generated by Django 5.0.3 on 2024-04-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0003_examen_detallado_alter_examen_descripcion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examen',
            old_name='nombre',
            new_name='titulo',
        ),
        migrations.AddField(
            model_name='examen',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='examen',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
