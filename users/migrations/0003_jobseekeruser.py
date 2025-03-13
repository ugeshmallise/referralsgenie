# Generated by Django 5.1.6 on 2025-03-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_first_name_user_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeekerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('company_name', models.CharField(max_length=50)),
                ('company_email', models.EmailField(max_length=254, unique=True)),
                ('personal_email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
