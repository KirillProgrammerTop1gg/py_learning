from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "text", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("title", "author__username")
    ordering = ("-created_at", "author", "title")
    readonly_fields = ("created_at", "updated_at")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "text", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("text", "author__username", "post__title")
    ordering = ("-created_at",)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
