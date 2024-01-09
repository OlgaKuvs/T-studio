# Generated by Django 3.2.21 on 2024-01-01 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('profile_street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('profile_city', models.CharField(blank=True, max_length=40, null=True)),
                ('profile_county', models.CharField(blank=True, choices=[('', 'Choose a county*'), ('carlow', 'Carlow'), ('cavan', 'Cavan'), ('clare', 'Clare'), ('cork', 'Cork'), ('donegal', 'Donegal'), ('dublin', 'Dublin'), ('galway', 'Galway'), ('kerry', 'Kerry'), ('kildare', 'Kildare'), ('kilkenny', 'Kilkenny'), ('laois', 'Laois'), ('leitrim', 'Leitrim'), ('limerick', 'Limerick'), ('longford', 'Longford'), ('louth', 'Louth'), ('mayo', 'Mayo'), ('meath', 'Meath'), ('monaghan', 'Monaghan'), ('offaly', 'Offaly'), ('roscommon', 'Roscommon'), ('sligo', 'Sligo'), ('tipperary', 'Tipperary'), ('waterford', 'Waterford'), ('westmeath', 'Westmeath'), ('wexford', 'Wexford'), ('wicklow', 'Wicklow')], max_length=80, null=True)),
                ('profile_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_country', models.CharField(blank=True, default='IE', max_length=50, null=True)),
                ('is_default', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile')),
            ],
        ),
    ]