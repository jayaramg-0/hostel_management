from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by', 'created_at']
    list_filter = ['status', 'date', 'student__department']
    search_fields = ['student__name', 'student__student_id']
    date_hierarchy = 'date'
    ordering = ['-date', 'student__name']
    list_per_page = 20
