from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from datetime import date, timedelta
from students.models import Student
from rooms.models import Room
from attendance.models import Attendance
from visitors.models import Visitor
from complaints.models import Complaint
from fees.models import Fee
from notices.models import Notice
from leave_requests.models import LeaveRequest


@login_required
def index(request):
    """Dashboard view based on user role"""
    if request.user.is_admin_user:
        return admin_dashboard(request)
    else:
        return student_dashboard(request)


def admin_dashboard(request):
    """Admin Dashboard"""
    today = date.today()
    
    # Student Statistics
    total_students = Student.objects.filter(is_active=True).count()
    students_by_department = Student.objects.filter(is_active=True).values('department').annotate(count=Count('id'))
    
    # Room Statistics
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(status='full').count()
    available_rooms = Room.objects.filter(status='available').count()
    total_capacity = Room.objects.aggregate(total=Sum('capacity'))['total'] or 0
    total_occupied = Room.objects.aggregate(total=Sum('occupied_beds'))['total'] or 0
    
    # Today's Statistics
    today_visitors = Visitor.objects.filter(entry_time__date=today).count()
    visitors_currently_in = Visitor.objects.filter(exit_time__isnull=True).count()
    
    # Pending Items
    pending_complaints = Complaint.objects.filter(status='pending').count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    
    # Fee Statistics
    total_fees = Fee.objects.aggregate(total=Sum('amount'))['total'] or 0
    collected_fees = Fee.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    pending_fees = Fee.objects.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent Activity
    recent_complaints = Complaint.objects.select_related('student')[:5]
    recent_leaves = LeaveRequest.objects.select_related('student')[:5]
    recent_visitors = Visitor.objects.select_related('student')[:5]
    
    # Attendance Today
    attendance_today = Attendance.objects.filter(date=today).count()
    present_today = Attendance.objects.filter(date=today, status='present').count()
    absent_today = Attendance.objects.filter(date=today, status='absent').count()
    
    context = {
        'total_students': total_students,
        'students_by_department': students_by_department,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'total_capacity': total_capacity,
        'total_occupied': total_occupied,
        'today_visitors': today_visitors,
        'visitors_currently_in': visitors_currently_in,
        'pending_complaints': pending_complaints,
        'pending_leaves': pending_leaves,
        'total_fees': total_fees,
        'collected_fees': collected_fees,
        'pending_fees': pending_fees,
        'recent_complaints': recent_complaints,
        'recent_leaves': recent_leaves,
        'recent_visitors': recent_visitors,
        'attendance_today': attendance_today,
        'present_today': present_today,
        'absent_today': absent_today,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


def student_dashboard(request):
    """Student Dashboard"""
    context = {}
    
    if hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
        context['student'] = student
        
        # Room Details
        context['room'] = student.room
        
        # Attendance
        context['attendance_percentage'] = student.get_attendance_percentage()
        
        # Recent Attendance
        recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
        context['recent_attendance'] = recent_attendance
        
        # Fees
        context['pending_fees'] = student.get_pending_fees()
        pending_fee_records = Fee.objects.filter(student=student, status='unpaid')[:5]
        context['pending_fee_records'] = pending_fee_records
        
        # Complaints
        recent_complaints = Complaint.objects.filter(student=student)[:5]
        context['recent_complaints'] = recent_complaints
        pending_complaints = Complaint.objects.filter(student=student, status='pending').count()
        context['pending_complaints_count'] = pending_complaints
        
        # Leave Requests
        recent_leaves = LeaveRequest.objects.filter(student=student)[:5]
        context['recent_leaves'] = recent_leaves
        pending_leaves = LeaveRequest.objects.filter(student=student, status='pending').count()
        context['pending_leaves_count'] = pending_leaves
        
        # Notices
        recent_notices = Notice.objects.filter(is_active=True)[:5]
        context['recent_notices'] = recent_notices
    else:
        context['no_profile'] = True
    
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def reports(request):
    """Reports Dashboard (Admin only)"""
    if not request.user.is_admin_user:
        return redirect('dashboard:index')
    
    report_type = request.GET.get('type', 'students')
    
    context = {
        'report_type': report_type,
    }
    
    if report_type == 'students':
        # Student Reports
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['students_by_department'] = Student.objects.filter(is_active=True).values('department').annotate(count=Count('id'))
        context['students_by_year'] = Student.objects.filter(is_active=True).values('year').annotate(count=Count('id'))
        context['students_by_gender'] = Student.objects.filter(is_active=True).values('gender').annotate(count=Count('id'))
        context['students_list'] = Student.objects.filter(is_active=True)
    
    elif report_type == 'rooms':
        # Room Reports
        context['total_rooms'] = Room.objects.count()
        context['available_rooms'] = Room.objects.filter(status='available').count()
        context['full_rooms'] = Room.objects.filter(status='full').count()
        context['rooms_by_floor'] = Room.objects.values('floor').annotate(count=Count('id'), capacity=Sum('capacity'), occupied=Sum('occupied_beds'))
        context['rooms_list'] = Room.objects.all()
    
    elif report_type == 'attendance':
        # Attendance Reports
        month = int(request.GET.get('month', date.today().month))
        year = int(request.GET.get('year', date.today().year))
        
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        context['month'] = month
        context['year'] = year
        
        students = Student.objects.filter(is_active=True)
        report_data = []
        for student in students:
            attendances = Attendance.objects.filter(student=student, date__gte=first_day, date__lte=last_day)
            total = attendances.count()
            present = attendances.filter(status='present').count()
            percentage = round((present / total) * 100, 2) if total > 0 else 0
            report_data.append({
                'student': student,
                'total': total,
                'present': present,
                'absent': total - present,
                'percentage': percentage
            })
        context['attendance_data'] = report_data
    
    elif report_type == 'fees':
        # Fee Reports
        context['total_fees'] = Fee.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['paid_fees'] = Fee.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
        context['unpaid_fees'] = Fee.objects.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
        context['fees_by_type'] = Fee.objects.values('fee_type').annotate(total=Sum('amount'), count=Count('id'))
        context['overdue_count'] = Fee.objects.filter(status='unpaid', due_date__lt=date.today()).count()
        context['unpaid_list'] = Fee.objects.filter(status='unpaid').select_related('student')
    
    elif report_type == 'complaints':
        # Complaint Reports
        context['total_complaints'] = Complaint.objects.count()
        context['pending'] = Complaint.objects.filter(status='pending').count()
        context['in_progress'] = Complaint.objects.filter(status='in_progress').count()
        context['resolved'] = Complaint.objects.filter(status='resolved').count()
        context['complaints_by_category'] = Complaint.objects.values('category').annotate(count=Count('id'))
        context['pending_list'] = Complaint.objects.filter(status__in=['pending', 'in_progress']).select_related('student')
    
    return render(request, 'dashboard/reports.html', context)
