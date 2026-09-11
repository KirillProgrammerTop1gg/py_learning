from django import forms
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Article, Tag
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "views",
        "likes",
        "is_featured",
        "published_at",
    ]

    list_filter = [
        "is_featured",
        "published_at",
        "author",
        "tags",
    ]

    search_fields = ["title", "content"]
    list_editable = ["is_featured"]
    filter_horizontal = ["tags"]
    readonly_fields = ["views", "likes"]

    actions = [
        "make_featured",
        "reset_views",
        "export_articles",
    ]

    @admin.action(description="Позначити як Featured")
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f"{updated} статей позначено як Featured."
        )

    @admin.action(description="Скинути лічильник переглядів")
    def reset_views(self, request, queryset):
        updated = queryset.update(views=0)
        self.message_user(
            request,
            f"Лічильник переглядів скинуто у {updated} статей."
        )

    @admin.action(description="Експорт вибраних статей у CSV")
    def export_articles(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="articles.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Title",
            "Author",
            "Views",
            "Likes",
            "Featured",
            "Published",
        ])

        for article in queryset:
            writer.writerow([
                article.title,
                article.author.username,
                article.views,
                article.likes,
                article.is_featured,
                article.published_at,
            ])

        return response

class TagAdminForm(forms.ModelForm):
    color = forms.CharField(
        widget=forms.TextInput(attrs={"type": "color"})
    )

    class Meta:
        model = Tag
        fields = "__all__"

class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm

    list_display = ["name", "color_preview", "color"]
    search_fields = ["name"]
    ordering = ["name"]

    @admin.display(description="Колір")
    def color_preview(self, obj):
        return mark_safe(
            f"""
            <div style="
                width:25px;
                height:25px;
                background:{obj.color};
                border:1px solid #999;
                border-radius:4px;
            "></div>
            """
        )
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)