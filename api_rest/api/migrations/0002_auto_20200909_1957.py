# Generated by Django 2.1.2 on 2020-09-10 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(max_length=300, verbose_name='Descripcion')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.CharField(max_length=25, verbose_name='Identificacion')),
                ('names', models.CharField(max_length=100, verbose_name='Nombres')),
                ('last_names', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('price', models.DecimalField(decimal_places=0, max_digits=15)),
                ('stock', models.DecimalField(decimal_places=0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=0, max_digits=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('document', models.CharField(max_length=50, verbose_name='Nit')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Persona',
        ),
        migrations.AddField(
            model_name='purchase',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Store'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Store'),
        ),
    ]
