# Generated by Django 3.2.21 on 2024-02-11 11:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='Please enter a correct phone number. Up to 15 digits without spaces allowed.', regex='^(\\+\\d{1,3})?,?\\s?\\d{7,15}$')]),
        ),
    ]
