from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import date
from .models import Fee
from .forms import FeeForm, FeePaymentForm, FeeFilterForm
from accounts.decorators import admin_required


@login_required
def fee_list(request):
    """List fees based on user role"""
    if request.user.is_admin_user:
        fees = Fee.objects.select_related('student')
    else:
        # Students see only their fees
        if hasattr(request.user, 'student_profile'):
            fees = Fee.objects.filter(student=request.user.student_profile)
        else:
            fees = Fee.objects.none()
    
    form = FeeFilterForm(request.GET)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        fee_type = form.cleaned_data.get('fee_type')
        status = form.cleaned_data.get('status')
        
        if student:
            fees = fees.filter(student=student)
        if fee_type:
            fees = fees.filter(fee_type=fee_type)
        if status:
            fees = fees.filter(status=status)
    
    # Statistics
    total_fees = fees.aggregate(total=Sum('amount'))['total'] or 0
    paid_fees = fees.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    unpaid_fees = fees.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
    overdue_count = fees.filter(status='unpaid', due_date__lt=date.today()).count()
    
    stats = {
        'total': total_fees,
        'paid': paid_fees,
        'unpaid': unpaid_fees,
        'overdue_count': overdue_count,
    }
    
    paginator = Paginator(fees, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'stats': stats,
    }
    return render(request, 'fees/fee_list.html', context)


@login_required
@admin_required
def fee_create(request):
    """Create new fee record"""
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save()
            messages.success(request, f'Fee record created for {fee.student.name}!')
            return redirect('fees:list')
    else:
        form = FeeForm()
    
    return render(request, 'fees/fee_form.html', {
        'form': form,
        'title': 'Add Fee Record',
        'button_text': 'Create Fee Record'
    })


@login_required
def fee_detail(request, pk):
    """View fee details"""
    fee = get_object_or_404(Fee, pk=pk)
    
    # Check permission for students
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or fee.student != request.user.student_profile:
            messages.error(request, 'You can only view your own fee records.')
            return redirect('fees:list')
    
    return render(request, 'fees/fee_detail.html', {'fee': fee})


@login_required
@admin_required
def fee_update(request, pk):
    """Update fee record"""
    fee = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record updated successfully!')
            return redirect('fees:detail', pk=fee.pk)
    else:
        form = FeeForm(instance=fee)
    
    return render(request, 'fees/fee_form.html', {
        'form': form,
        'fee': fee,
        'title': f'Edit Fee Record',
        'button_text': 'Update Fee Record'
    })


@login_required
@admin_required
def fee_delete(request, pk):
    """Delete fee record"""
    fee = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee record deleted successfully!')
        return redirect('fees:list')
    
    return render(request, 'fees/fee_confirm_delete.html', {'fee': fee})


@login_required
@admin_required
def fee_update_payment(request, pk):
    """Update payment status"""
    fee = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=fee)
        if form.is_valid():
            fee = form.save(commit=False)
            if fee.status == 'paid' and not fee.payment_date:
                fee.payment_date = date.today()
            fee.save()
            messages.success(request, 'Payment status updated successfully!')
            return redirect('fees:detail', pk=fee.pk)
    else:
        form = FeePaymentForm(instance=fee)
    
    return render(request, 'fees/fee_payment_update.html', {
        'form': form,
        'fee': fee,
    })


@login_required
def student_fees(request, pk):
    """View all fees for a specific student"""
    from students.models import Student
    student = get_object_or_404(Student, pk=pk)
    
    # Check permission for students
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or request.user.student_profile.pk != pk:
            messages.error(request, 'You can only view your own fee records.')
            return redirect('dashboard:index')
    
    fees = Fee.objects.filter(student=student)
    
    # Statistics
    total_fees = fees.aggregate(total=Sum('amount'))['total'] or 0
    paid_fees = fees.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    unpaid_fees = fees.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
    
    paginator = Paginator(fees, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'student': student,
        'page_obj': page_obj,
        'total_fees': total_fees,
        'paid_fees': paid_fees,
        'unpaid_fees': unpaid_fees,
    }
    return render(request, 'fees/student_fees.html', context)
