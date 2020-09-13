# Generated by Django 3.1.1 on 2020-09-10 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200910_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackpoint',
            name='sendero',
        ),
        migrations.AddField(
            model_name='trackpoint',
            name='sendero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.gpxtrack'),
        ),
    ]
