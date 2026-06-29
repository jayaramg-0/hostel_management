from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'posted_by', 'posted_date', 'is_active']
    list_filter = ['priority', 'is_active', 'posted_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'posted_date'
    ordering = ['-posted_date']
    list_per_page = 20
    readonly_fields = ['posted_by', 'posted_date', 'updated_at']
    
    def get_fields(self, request, obj=None):
        if obj:  # Editing existing
            return ['title', 'description', 'priority', 'attachment', 'is_active', 'posted_by', 'posted_date', 'updated_at']
        else:  # Creating new
            return ['title', 'description', 'priority', 'attachment', 'is_active']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new notice
            obj.posted_by = request.user
        super().save_model(request, obj, form, change)
