# Generated by Django 5.0.3 on 2024-04-14 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0007_rename_titulo_examen_nombre_remove_examen_imagen_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='imagen_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
