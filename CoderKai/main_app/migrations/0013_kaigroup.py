# Generated by Django 4.2.2 on 2023-08-14 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0012_rename_postvote_postkudos_responsekudos'),
    ]

    operations = [
        migrations.CreateModel(
            name='KaiGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('about', models.TextField(help_text='Short info about the group', max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL)),
                ('interests', models.ManyToManyField(to='main_app.interest')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('motivations', models.ManyToManyField(to='main_app.motivation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
