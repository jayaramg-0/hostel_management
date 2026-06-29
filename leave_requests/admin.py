from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'leave_type', 'from_date', 'to_date', 'duration_days', 'status', 'approved_by', 'created_at']
    list_filter = ['leave_type', 'status', 'from_date']
    search_fields = ['student__name', 'student__student_id', 'reason']
    date_hierarchy = 'from_date'
    ordering = ['-created_at']
    list_per_page = 20
