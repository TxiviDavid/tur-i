# Generated by Django 3.1.14 on 2023-02-04 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20230204_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subregion',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.region'),
        ),
    ]
