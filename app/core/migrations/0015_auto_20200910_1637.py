# Generated by Django 3.1.1 on 2020-09-10 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200910_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpxpoint',
            name='gpx_fichero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gpxfile'),
        ),
        migrations.AlterField(
            model_name='gpxtrack',
            name='gpx_fichero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gpxfile'),
        ),
    ]