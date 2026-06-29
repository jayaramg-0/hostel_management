from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_id', 'student', 'category', 'subject', 'status', 'created_at', 'resolved_date']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['complaint_id', 'subject', 'student__name']
    readonly_fields = ['complaint_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20
