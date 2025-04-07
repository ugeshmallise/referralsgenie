# Generated by Django 5.1.6 on 2025-04-07 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobProviderProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_description', models.TextField(blank=True, null=True)),
                ('badge', models.CharField(default='New Provider', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobprovider_profile', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('experience', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('badge', models.CharField(default='New User', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_profile', to='users.user')),
            ],
        ),
    ]
