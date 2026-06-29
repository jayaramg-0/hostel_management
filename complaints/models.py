from django.db import models
from students.models import Student


class Complaint(models.Model):
    """Complaint Model"""
    
    CATEGORY_CHOICES = (
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('internet', 'Internet'),
        ('cleaning', 'Cleaning'),
        ('furniture', 'Furniture'),
        ('security', 'Security'),
        ('food', 'Food'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    complaint_id = models.CharField(max_length=20, unique=True, editable=False)
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='complaints'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, null=True)
    resolved_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
    
    def save(self, *args, **kwargs):
        if not self.complaint_id:
            # Generate complaint ID
            last_complaint = Complaint.objects.order_by('-id').first()
            if last_complaint:
                last_id = int(last_complaint.complaint_id.replace('CMP', ''))
                self.complaint_id = f'CMP{str(last_id + 1).zfill(5)}'
            else:
                self.complaint_id = 'CMP00001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.complaint_id} - {self.subject}"
