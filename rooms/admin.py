from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor', 'capacity', 'occupied_beds', 'available_beds', 'status']
    list_filter = ['floor', 'status']
    search_fields = ['room_number']
    ordering = ['floor', 'room_number']
    list_per_page = 20
    
    readonly_fields = ['occupied_beds', 'status']
