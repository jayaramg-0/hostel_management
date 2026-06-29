from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import Complaint
from .forms import ComplaintForm, ComplaintUpdateForm, ComplaintFilterForm
from accounts.decorators import admin_required, student_required


@login_required
def complaint_list(request):
    """List complaints based on user role"""
    if request.user.is_admin_user:
        complaints = Complaint.objects.select_related('student')
    else:
        # Students see only their complaints
        if hasattr(request.user, 'student_profile'):
            complaints = Complaint.objects.filter(student=request.user.student_profile)
        else:
            complaints = Complaint.objects.none()
    
    form = ComplaintFilterForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        
        if search:
            complaints = complaints.filter(
                Q(complaint_id__icontains=search) |
                Q(subject__icontains=search) |
                Q(student__name__icontains=search)
            )
        if category:
            complaints = complaints.filter(category=category)
        if status:
            complaints = complaints.filter(status=status)
    
    # Statistics
    stats = {
        'total': complaints.count(),
        'pending': complaints.filter(status='pending').count(),
        'in_progress': complaints.filter(status='in_progress').count(),
        'resolved': complaints.filter(status='resolved').count(),
    }
    
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'stats': stats,
    }
    return render(request, 'complaints/complaint_list.html', context)


@login_required
@student_required
def complaint_create(request):
    """Submit new complaint (Student only)"""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'Your student profile is not set up. Please contact admin.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user.student_profile
            complaint.save()
            messages.success(request, f'Complaint submitted successfully! ID: {complaint.complaint_id}')
            return redirect('complaints:list')
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/complaint_form.html', {
        'form': form,
        'title': 'Submit New Complaint',
        'button_text': 'Submit Complaint'
    })


@login_required
def complaint_detail(request, pk):
    """View complaint details"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permission for students
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or complaint.student != request.user.student_profile:
            messages.error(request, 'You can only view your own complaints.')
            return redirect('complaints:list')
    
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})


@login_required
@admin_required
def complaint_update(request, pk):
    """Update complaint status (Admin only)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            if complaint.status == 'resolved' and not complaint.resolved_date:
                complaint.resolved_date = timezone.now()
            complaint.save()
            messages.success(request, 'Complaint updated successfully!')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintUpdateForm(instance=complaint)
    
    return render(request, 'complaints/complaint_update.html', {
        'form': form,
        'complaint': complaint,
    })


@login_required
@admin_required
def complaint_resolve(request, pk):
    """Quick resolve complaint (Admin only)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        complaint.status = 'resolved'
        complaint.resolved_date = timezone.now()
        complaint.admin_remarks = request.POST.get('remarks', 'Resolved by admin')
        complaint.save()
        messages.success(request, f'Complaint {complaint.complaint_id} resolved!')
        return redirect('complaints:list')
    
    return render(request, 'complaints/complaint_resolve_confirm.html', {'complaint': complaint})
