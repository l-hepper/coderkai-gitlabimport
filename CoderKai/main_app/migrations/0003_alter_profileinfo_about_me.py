# Generated by Django 4.2.2 on 2023-08-06 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_profileinfo_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileinfo',
            name='about_me',
            field=models.TextField(max_length=64),
        ),
    ]