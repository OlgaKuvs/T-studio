# Generated by Django 3.2.21 on 2024-01-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='profile_country',
            field=models.CharField(default='IE', max_length=50),
        ),
    ]
