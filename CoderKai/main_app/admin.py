from django.contrib import admin

from main_app.models import Interest, Motivation, Post, ProfileInfo, Tag

# Register your models here.


admin.site.register(ProfileInfo)
admin.site.register(Interest)
admin.site.register(Motivation)
admin.site.register(Post)
admin.site.register(Tag)