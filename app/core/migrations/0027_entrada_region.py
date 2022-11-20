# Generated by Django 3.1.14 on 2022-11-18 20:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20221106_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.IntegerField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.IntegerField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.region')),
            ],
        ),
    ]
