from django.contrib import admin

from main_app.models import Interest, Motivation

# Register your models here.

admin.site.register(Motivation)
admin.site.register(Interest)