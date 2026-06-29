from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import LeaveRequest
from .forms import LeaveRequestForm, LeaveApprovalForm, LeaveFilterForm
from accounts.decorators import admin_required, student_required


@login_required
def leave_list(request):
    """List leave requests based on user role"""
    if request.user.is_admin_user:
        leaves = LeaveRequest.objects.select_related('student', 'approved_by')
    else:
        # Students see only their leave requests
        if hasattr(request.user, 'student_profile'):
            leaves = LeaveRequest.objects.filter(student=request.user.student_profile)
        else:
            leaves = LeaveRequest.objects.none()
    
    form = LeaveFilterForm(request.GET)
    
    if form.is_valid():
        status = form.cleaned_data.get('status')
        leave_type = form.cleaned_data.get('leave_type')
        
        if status:
            leaves = leaves.filter(status=status)
        if leave_type:
            leaves = leaves.filter(leave_type=leave_type)
    
    # Statistics
    stats = {
        'total': leaves.count(),
        'pending': leaves.filter(status='pending').count(),
        'approved': leaves.filter(status='approved').count(),
        'rejected': leaves.filter(status='rejected').count(),
    }
    
    paginator = Paginator(leaves, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'stats': stats,
    }
    return render(request, 'leave_requests/leave_list.html', context)


@login_required
@student_required
def leave_create(request):
    """Submit leave request (Student only)"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Your student profile is not set up. Please contact admin.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = request.user.student_profile
            leave.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('leave_requests:list')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leave_requests/leave_form.html', {
        'form': form,
        'title': 'Apply for Leave',
        'button_text': 'Submit Request'
    })


@login_required
def leave_detail(request, pk):
    """View leave request details"""
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    # Check permission for students
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or leave.student != request.user.student_profile:
            messages.error(request, 'You can only view your own leave requests.')
            return redirect('leave_requests:list')
    
    return render(request, 'leave_requests/leave_detail.html', {'leave': leave})


@login_required
@admin_required
def leave_approve(request, pk):
    """Approve/Reject leave request (Admin only)"""
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.approved_by = request.user
            leave.save()
            
            # Send email notification (optional)
            try:
                if leave.student.email:
                    send_mail(
                        subject=f'Leave Request {leave.get_status_display()}',
                        message=f'Your leave request from {leave.from_date} to {leave.to_date} has been {leave.get_status_display().lower()}.\n\nRemarks: {leave.admin_remarks or "None"}',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[leave.student.email],
                        fail_silently=True,
                    )
            except:
                pass
            
            messages.success(request, f'Leave request {leave.get_status_display().lower()}!')
            return redirect('leave_requests:list')
    else:
        form = LeaveApprovalForm(instance=leave)
    
    return render(request, 'leave_requests/leave_approve.html', {
        'form': form,
        'leave': leave,
    })


@login_required
@admin_required
def leave_quick_approve(request, pk):
    """Quick approve leave request"""
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave request approved!')
    
    return redirect('leave_requests:list')


@login_required
@admin_required
def leave_quick_reject(request, pk):
    """Quick reject leave request"""
    leave = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        leave.status = 'rejected'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave request rejected!')
    
    return redirect('leave_requests:list')


@login_required
def leave_history(request, student_pk):
    """View leave history for a specific student"""
    from students.models import Student
    student = get_object_or_404(Student, pk=student_pk)
    
    # Check permission for students
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or request.user.student_profile.pk != student_pk:
            messages.error(request, 'You can only view your own leave history.')
            return redirect('dashboard:index')
    
    leaves = LeaveRequest.objects.filter(student=student)
    
    paginator = Paginator(leaves, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'student': student,
        'page_obj': page_obj,
    }
    return render(request, 'leave_requests/leave_history.html', context)
