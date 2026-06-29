from django.contrib import admin
from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount', 'due_date', 'status', 'payment_date', 'is_overdue']
    list_filter = ['fee_type', 'status', 'due_date']
    search_fields = ['student__name', 'student__student_id', 'transaction_id']
    date_hierarchy = 'due_date'
    ordering = ['-due_date']
    list_per_page = 20
