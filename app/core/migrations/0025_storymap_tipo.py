# Generated by Django 3.1.14 on 2022-10-22 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_storymap'),
    ]

    operations = [
        migrations.AddField(
            model_name='storymap',
            name='tipo',
            field=models.CharField(choices=[('HISTORIA', 'Historia'), ('MITOLOGIA', 'Mitologia'), ('FOLCLORE', 'Folclore'), ('MUSICA', 'Musica'), ('DEPORTE', 'Deporte')], default='HISTORIA', max_length=50),
        ),
    ]
