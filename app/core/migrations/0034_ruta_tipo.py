# Generated by Django 3.1.14 on 2023-01-24 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_ruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
