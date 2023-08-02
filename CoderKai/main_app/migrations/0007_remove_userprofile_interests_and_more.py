# Generated by Django 4.2.2 on 2023-08-02 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_remove_interest_users_remove_motivation_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='motivations',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Interest',
        ),
        migrations.DeleteModel(
            name='Motivation',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
