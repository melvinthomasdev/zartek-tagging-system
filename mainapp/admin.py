from atexit import register
from pyexpat import model
from statistics import mode
from django.contrib import admin

from mainapp.models import Post, PostImage, Tag, PostTag, Vote


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class TagAdmin(admin.ModelAdmin):

    class Meta:
        model = Tag

class PostTagAdmin(admin.StackedInline):
    model = PostTag


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin, PostTagAdmin ]
    list_display = ['title', 'description', 'number_of_likes', 'number_of_dislikes']

    class Meta:
        model = Post

admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Vote)