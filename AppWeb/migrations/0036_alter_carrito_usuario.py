# Generated by Django 5.0.3 on 2024-05-17 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0035_comprahistorica_delete_historialcompra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
