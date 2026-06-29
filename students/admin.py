from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'department', 'year', 'room', 'phone', 'is_active']
    list_filter = ['department', 'year', 'gender', 'is_active']
    search_fields = ['student_id', 'name', 'email', 'phone']
    ordering = ['name']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'student_id', 'name', 'gender', 'date_of_birth', 'profile_photo')
        }),
        ('Academic Information', {
            'fields': ('department', 'year')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Parent Information', {
            'fields': ('parent_name', 'parent_contact')
        }),
        ('Hostel Information', {
            'fields': ('room', 'is_active')
        }),
    )
