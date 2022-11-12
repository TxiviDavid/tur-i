# Generated by Django 3.1.14 on 2022-11-06 10:59

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_storymap_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='creationDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='plan',
            name='modificationDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='PlanMovil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('plan', models.JSONField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to=core.models.plan_image_file_path)),
                ('descripcion', models.CharField(blank=True, max_length=254, null=True)),
                ('shared', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('modificationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PlanMovil',
                'verbose_name_plural': 'PlanesMovil',
            },
        ),
    ]
