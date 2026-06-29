from django.db import models


class Room(models.Model):
    """Room Model"""
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('full', 'Full'),
    )
    
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=4)
    occupied_beds = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['floor', 'room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor})"
    
    def update_occupancy(self):
        """Update occupied beds count and status"""
        self.occupied_beds = self.students.filter(is_active=True).count()
        if self.occupied_beds >= self.capacity:
            self.status = 'full'
        else:
            self.status = 'available'
        self.save()
    
    @property
    def available_beds(self):
        """Return number of available beds"""
        return self.capacity - self.occupied_beds
    
    @property
    def occupancy_percentage(self):
        """Return occupancy percentage"""
        if self.capacity == 0:
            return 0
        return round((self.occupied_beds / self.capacity) * 100, 2)
