from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Notice
from .forms import NoticeForm
from accounts.decorators import admin_required


@login_required
def notice_list(request):
    """List all notices"""
    if request.user.is_admin_user:
        notices = Notice.objects.all()
    else:
        notices = Notice.objects.filter(is_active=True)
    
    # Filter by priority
    priority = request.GET.get('priority', '')
    if priority:
        notices = notices.filter(priority=priority)
    
    paginator = Paginator(notices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'priority': priority,
    }
    return render(request, 'notices/notice_list.html', context)


@login_required
@admin_required
def notice_create(request):
    """Create new notice"""
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            messages.success(request, 'Notice created successfully!')
            return redirect('notices:list')
    else:
        form = NoticeForm()
    
    return render(request, 'notices/notice_form.html', {
        'form': form,
        'title': 'Create New Notice',
        'button_text': 'Post Notice'
    })


@login_required
def notice_detail(request, pk):
    """View notice details"""
    notice = get_object_or_404(Notice, pk=pk)
    
    # Students can only view active notices
    if request.user.is_student_user and not notice.is_active:
        messages.error(request, 'This notice is not available.')
        return redirect('notices:list')
    
    return render(request, 'notices/notice_detail.html', {'notice': notice})


@login_required
@admin_required
def notice_update(request, pk):
    """Update notice"""
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notices:detail', pk=notice.pk)
    else:
        form = NoticeForm(instance=notice)
    
    return render(request, 'notices/notice_form.html', {
        'form': form,
        'notice': notice,
        'title': f'Edit Notice',
        'button_text': 'Update Notice'
    })


@login_required
@admin_required
def notice_delete(request, pk):
    """Delete notice"""
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notices:list')
    
    return render(request, 'notices/notice_confirm_delete.html', {'notice': notice})
