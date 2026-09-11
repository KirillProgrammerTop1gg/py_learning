from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Skill, Experience, Technology, Category, PageView

class SliderAndNumberWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        value = value if value is not None else 80
        attrs = attrs or {}
        input_id = attrs.get('id', f'id_{name}')
        slider_id = f"{input_id}_slider"
        number_id = input_id

        html = format_html(
            '<div style="display: inline-flex; align-items: center; gap: 10px; white-space: nowrap; vertical-align: middle;">'
            '<input type="range" id="{}" min="0" max="100" step="1" value="{}" style="width: 120px; margin: 0; vertical-align: middle;" '
            'oninput="document.getElementById(\'{}\').value = this.value;">'
            '<input type="number" name="{}" id="{}" min="0" max="100" value="{}" style="width: 55px; text-align: center; vertical-align: middle; padding: 3px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace;" '
            'oninput="document.getElementById(\'{}\').value = this.value;">'
            '</div>',
            slider_id, value, number_id,
            name, number_id, value, slider_id
        )
        return html


class SkillAdminForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        widgets = {
            'level': SliderAndNumberWidget()
        }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "display_technologies", "github_link", "views_count")
    list_editable = ("date", "github_link")
    list_filter = ("date", "technologies")
    search_fields = ("name", "description", "technologies__name")
    date_hierarchy = "date"
    filter_horizontal = ("technologies",)  # Зручний горизонтальний віджет вибору ManyToMany

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('technologies')

    @admin.display(description="Технології")
    def display_technologies(self, obj):
        return ", ".join([tech.name for tech in obj.technologies.all()])


class SkillAdmin(admin.ModelAdmin):
    form = SkillAdminForm
    list_display = ("name", "level_progress_bar", "level", "category")
    list_editable = ("level", "category")
    list_filter = ("category",)
    search_fields = ("name", "category__name")

    @admin.display(description="Прогрес")
    def level_progress_bar(self, obj):
        return format_html(
            '<div style="width: 120px; background-color: #3a2f22; border-radius: 6px; overflow: hidden; display: inline-block; vertical-align: middle; height: 12px; border: 1px solid #3a2f22; margin-right: 8px;">'
            '<div style="width: {}%; background-color: #e8a33d; height: 100%; box-shadow: 0 0 5px rgba(232, 163, 61, 0.4);"></div>'
            '</div>'
            '<span style="font-family: monospace; font-weight: bold; color: #e8a33d;">{}%</span>',
            obj.level, obj.level
        )


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "period", "start_date")
    list_editable = ("period", "start_date")
    list_filter = ("company",)
    search_fields = ("position", "company", "description")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Experience, ExperienceAdmin)

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "views_count", "last_viewed")
    ordering = ("-views_count",)