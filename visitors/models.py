from django.db import models
from students.models import Student


class Visitor(models.Model):
    """Visitor Model"""
    
    RELATIONSHIP_CHOICES = (
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('sibling', 'Sibling'),
        ('relative', 'Relative'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    )
    
    visitor_name = models.CharField(max_length=100)
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='visitors'
    )
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    phone = models.CharField(max_length=15)
    purpose = models.CharField(max_length=200, blank=True, null=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(blank=True, null=True)
    id_proof = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-entry_time']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
    
    def __str__(self):
        return f"{self.visitor_name} → {self.student.name}"
    
    @property
    def is_checked_out(self):
        """Check if visitor has checked out"""
        return self.exit_time is not None
