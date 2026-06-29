from django.db import models
from students.models import Student


class Fee(models.Model):
    """Fee Model"""
    
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    )
    
    FEE_TYPE_CHOICES = (
        ('hostel', 'Hostel Fee'),
        ('mess', 'Mess Fee'),
        ('maintenance', 'Maintenance Fee'),
        ('security', 'Security Deposit'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='fees'
    )
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='hostel')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'
    
    def __str__(self):
        return f"{self.student.name} - {self.get_fee_type_display()} - ₹{self.amount}"
    
    @property
    def is_overdue(self):
        """Check if fee is overdue"""
        from datetime import date
        return self.status == 'unpaid' and self.due_date < date.today()
