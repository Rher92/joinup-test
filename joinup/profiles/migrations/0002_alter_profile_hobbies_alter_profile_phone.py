# Generated by Django 4.0.5 on 2022-06-13 14:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hobbies',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.RegexValidator(message='Formato requerido: +999999999.', regex='\\+?1?\\d{9,15}$')]),
        ),
    ]
