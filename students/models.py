from django.db import models
from django.conf import settings


class Student(models.Model):
    """Student Model"""
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    YEAR_CHOICES = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        null=True,
        blank=True
    )
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    room = models.ForeignKey(
        'rooms.Room', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_id} - {self.name}"
    
    def get_attendance_percentage(self):
        """Calculate attendance percentage"""
        from attendance.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status='present').count()
        return round((present / total) * 100, 2)
    
    def get_pending_fees(self):
        """Get total pending fees"""
        from fees.models import Fee
        pending = Fee.objects.filter(student=self, status='unpaid').aggregate(
            total=models.Sum('amount')
        )
        return pending['total'] or 0
