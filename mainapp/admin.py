from atexit import register
from pyexpat import model
from statistics import mode
from django.contrib import admin

from mainapp.models import Profile, Post, PostImage, Tag, PostTag


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class TagAdmin(admin.ModelAdmin):

    class Meta:
        model = Tag

class PostTagAdmin(admin.StackedInline):
    model = PostTag


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin, PostTagAdmin ]

    class Meta:
        model = Post

admin.site.register(Post,PostAdmin)
admin.site.register(Profile)
admin.site.register(Tag)