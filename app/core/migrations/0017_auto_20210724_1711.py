# Generated by Django 3.1.13 on 2021-07-24 17:11

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200913_1100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntointeres',
            name='foto',
        ),
        migrations.CreateModel(
            name='PuntosInteresImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.punto_interes_image_file_path)),
                ('puntoInteres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.puntointeres')),
            ],
            options={
                'verbose_name': 'Material multimedia de los puntos de interés',
                'verbose_name_plural': 'Materiales multimedia de los puntos de interés',
            },
        ),
    ]
