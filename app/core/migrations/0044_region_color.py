# Generated by Django 3.1.14 on 2023-02-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_subregion_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]