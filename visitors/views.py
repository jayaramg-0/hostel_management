from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from datetime import date
from .models import Visitor
from .forms import VisitorForm, VisitorFilterForm
from accounts.decorators import admin_required


@login_required
@admin_required
def visitor_list(request):
    """List all visitors with filtering"""
    visitors = Visitor.objects.select_related('student')
    form = VisitorFilterForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        filter_date = form.cleaned_data.get('date')
        status = form.cleaned_data.get('status')
        
        if search:
            visitors = visitors.filter(
                Q(visitor_name__icontains=search) |
                Q(student__name__icontains=search)
            )
        if filter_date:
            visitors = visitors.filter(entry_time__date=filter_date)
        if status == 'in':
            visitors = visitors.filter(exit_time__isnull=True)
        elif status == 'out':
            visitors = visitors.filter(exit_time__isnull=False)
    
    # Count today's visitors
    today = date.today()
    today_visitors = Visitor.objects.filter(entry_time__date=today).count()
    currently_in = Visitor.objects.filter(exit_time__isnull=True).count()
    
    paginator = Paginator(visitors, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'today_visitors': today_visitors,
        'currently_in': currently_in,
    }
    return render(request, 'visitors/visitor_list.html', context)


@login_required
@admin_required
def visitor_create(request):
    """Register new visitor"""
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.entry_time = timezone.now()
            visitor.save()
            messages.success(request, f'Visitor {visitor.visitor_name} registered successfully!')
            return redirect('visitors:list')
    else:
        form = VisitorForm()
    
    return render(request, 'visitors/visitor_form.html', {
        'form': form,
        'title': 'Register New Visitor',
        'button_text': 'Register Visitor'
    })


@login_required
@admin_required
def visitor_detail(request, pk):
    """View visitor details"""
    visitor = get_object_or_404(Visitor, pk=pk)
    return render(request, 'visitors/visitor_detail.html', {'visitor': visitor})


@login_required
@admin_required
def visitor_checkout(request, pk):
    """Record visitor exit time"""
    visitor = get_object_or_404(Visitor, pk=pk)
    
    if visitor.exit_time:
        messages.warning(request, 'This visitor has already checked out.')
        return redirect('visitors:list')
    
    if request.method == 'POST':
        visitor.exit_time = timezone.now()
        visitor.save()
        messages.success(request, f'Visitor {visitor.visitor_name} checked out successfully!')
        return redirect('visitors:list')
    
    return render(request, 'visitors/visitor_checkout_confirm.html', {'visitor': visitor})


@login_required
@admin_required
def visitor_history(request, student_pk):
    """View visitor history for a specific student"""
    from students.models import Student
    student = get_object_or_404(Student, pk=student_pk)
    visitors = Visitor.objects.filter(student=student)
    
    paginator = Paginator(visitors, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'student': student,
        'page_obj': page_obj,
    }
    return render(request, 'visitors/visitor_history.html', context)
