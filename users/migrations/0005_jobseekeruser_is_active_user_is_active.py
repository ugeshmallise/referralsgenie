# Generated by Django 5.1.6 on 2025-03-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_personal_email_jobseekeruser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekeruser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
