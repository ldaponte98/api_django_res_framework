# Generated by Django 2.1.2 on 2020-09-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('names', models.CharField(max_length=100, verbose_name='Nombres')),
                ('last_names', models.CharField(max_length=150, verbose_name='Apellidos')),
            ],
        ),
    ]
