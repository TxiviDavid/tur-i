# Generated by Django 3.1.14 on 2023-01-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_ruta_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='gpx',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ruta',
            name='gpx',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
