from django.db import models
from students.models import Student


class LeaveRequest(models.Model):
    """Leave Request Model"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    LEAVE_TYPE_CHOICES = (
        ('home', 'Going Home'),
        ('medical', 'Medical Leave'),
        ('emergency', 'Emergency'),
        ('event', 'Event/Function'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='home')
    reason = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    destination = models.CharField(max_length=200, blank=True, null=True)
    contact_during_leave = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
    
    def __str__(self):
        return f"{self.student.name} - {self.from_date} to {self.to_date}"
    
    @property
    def duration_days(self):
        """Calculate leave duration in days"""
        return (self.to_date - self.from_date).days + 1
