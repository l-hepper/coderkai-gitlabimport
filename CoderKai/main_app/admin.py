from django.contrib import admin

from main_app.models import Interest, Motivation, ProfileInfo

# Register your models here.


admin.site.register(ProfileInfo)
admin.site.register(Interest)
admin.site.register(Motivation)