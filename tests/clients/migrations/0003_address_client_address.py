# Generated by Django 5.0.6 on 2024-07-27 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name': 'street',
                'verbose_name_plural': 'streets',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.address'),
        ),
    ]
