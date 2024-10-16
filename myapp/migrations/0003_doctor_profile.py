# Generated by Django 5.0 on 2024-01-09 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_profile_picture_user_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.CharField(max_length=100)),
                ('specialization', models.CharField(max_length=100)),
                ('experience_in_years', models.PositiveIntegerField()),
                ('clinic_address', models.TextField()),
                ('time', models.CharField(max_length=100)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
