from django.contrib import admin
from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'student', 'relationship', 'phone', 'entry_time', 'exit_time', 'is_checked_out']
    list_filter = ['relationship', 'entry_time']
    search_fields = ['visitor_name', 'student__name', 'phone']
    date_hierarchy = 'entry_time'
    ordering = ['-entry_time']
    list_per_page = 20
