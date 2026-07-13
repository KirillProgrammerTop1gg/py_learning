from django.contrib import admin
from .models import Order, Review

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project_name', 'project_type', 'budget', 'timeline', 'status', 'created_at')
    list_filter = ('status', 'project_type', 'created_at')
    search_fields = ('project_name', 'description', 'contacts', 'user__username', 'user__email')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'order__project_name', 'text')
    ordering = ('-created_at',)
