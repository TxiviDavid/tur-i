# Generated by Django 3.1 on 2020-09-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_restaurante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurante',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
    ]