# Generated by Django 3.1.14 on 2023-01-24 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20221128_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('puntos', models.JSONField()),
                ('path', models.JSONField()),
                ('gpx', models.JSONField()),
                ('shared', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('modificationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
