# Generated by Django 3.1.14 on 2023-02-07 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_region_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='planmovil',
            name='savedPlan',
            field=models.IntegerField(default=False, null=True),
        ),
    ]
