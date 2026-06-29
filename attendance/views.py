from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Attendance
from .forms import AttendanceFilterForm
from students.models import Student
from accounts.decorators import admin_required


@login_required
@admin_required
def attendance_list(request):
    """List attendance records with filtering"""
    attendances = Attendance.objects.select_related('student', 'marked_by')
    form = AttendanceFilterForm(request.GET)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        status = form.cleaned_data.get('status')
        
        if student:
            attendances = attendances.filter(student=student)
        if from_date:
            attendances = attendances.filter(date__gte=from_date)
        if to_date:
            attendances = attendances.filter(date__lte=to_date)
        if status:
            attendances = attendances.filter(status=status)
    
    paginator = Paginator(attendances, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
@admin_required
def mark_attendance(request):
    """Mark daily attendance for all students"""
    students = Student.objects.filter(is_active=True, room__isnull=False).order_by('name')
    today = date.today()
    
    # Check if attendance already marked for today
    existing_attendance = Attendance.objects.filter(date=today)
    existing_dict = {a.student_id: a.status for a in existing_attendance}
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date', today)
        
        for student in students:
            status = request.POST.get(f'student_{student.pk}', 'present')
            
            # Update or create attendance record
            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    'status': status,
                    'marked_by': request.user
                }
            )
        
        messages.success(request, f'Attendance marked successfully for {attendance_date}!')
        return redirect('attendance:list')
    
    context = {
        'students': students,
        'today': today,
        'existing_attendance': existing_dict,
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def attendance_report(request):
    """Monthly attendance report"""
    # Get month and year from query params or use current
    month = int(request.GET.get('month', date.today().month))
    year = int(request.GET.get('year', date.today().year))
    
    # Calculate date range
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    # Get students based on user role
    if request.user.is_admin_user:
        students = Student.objects.filter(is_active=True)
    else:
        # Student can only see their own report
        if hasattr(request.user, 'student_profile'):
            students = Student.objects.filter(pk=request.user.student_profile.pk)
        else:
            students = Student.objects.none()
    
    # Build report data
    report_data = []
    for student in students:
        attendances = Attendance.objects.filter(
            student=student,
            date__gte=first_day,
            date__lte=last_day
        )
        total = attendances.count()
        present = attendances.filter(status='present').count()
        absent = total - present
        percentage = round((present / total) * 100, 2) if total > 0 else 0
        
        report_data.append({
            'student': student,
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': percentage
        })
    
    # Generate list of months for dropdown
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # Generate list of years
    current_year = date.today().year
    years = range(current_year - 2, current_year + 1)
    
    context = {
        'report_data': report_data,
        'month': month,
        'year': year,
        'months': months,
        'years': years,
        'first_day': first_day,
        'last_day': last_day,
    }
    return render(request, 'attendance/attendance_report.html', context)


@login_required
def student_attendance(request, pk):
    """View attendance for specific student"""
    student = Student.objects.get(pk=pk)
    
    # Check permission
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or request.user.student_profile.pk != pk:
            messages.error(request, 'You can only view your own attendance.')
            return redirect('dashboard:index')
    
    attendances = Attendance.objects.filter(student=student).order_by('-date')
    
    paginator = Paginator(attendances, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'student': student,
        'page_obj': page_obj,
        'attendance_percentage': student.get_attendance_percentage(),
    }
    return render(request, 'attendance/student_attendance.html', context)
