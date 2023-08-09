from django.contrib import admin

from main_app.models import Interest, Motivation, Post, ProfileInfo, Reply, Response, Tag

# Register your models here.


admin.site.register(ProfileInfo)
admin.site.register(Interest)
admin.site.register(Motivation)
admin.site.register(Post)
admin.site.register(Response)
admin.site.register(Reply)
admin.site.register(Tag)