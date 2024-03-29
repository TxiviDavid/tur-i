# Generated by Django 3.1.14 on 2022-11-18 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_entrada_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrada',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='region',
        ),
        migrations.AddField(
            model_name='entrada',
            name='region',
            field=models.ManyToManyField(to='core.Region'),
        ),
        migrations.AlterField(
            model_name='region',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
