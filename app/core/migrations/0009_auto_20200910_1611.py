# Generated by Django 3.1.1 on 2020-09-10 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200910_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackpoint',
            name='sendero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gpxtrack'),
        ),
    ]