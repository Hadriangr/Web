# Generated by Django 5.0.3 on 2024-05-07 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppWeb', '0027_derivacion_alter_categoria_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('Derivacion', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppWeb.derivacion')),
            ],
        ),
    ]
