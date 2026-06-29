from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student
from .forms import StudentForm, StudentSearchForm
from accounts.decorators import admin_required


@login_required
@admin_required
def student_list(request):
    """List all students with search and pagination"""
    students = Student.objects.all()
    form = StudentSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        department = form.cleaned_data.get('department')
        year = form.cleaned_data.get('year')
        
        if search:
            students = students.filter(
                Q(name__icontains=search) |
                Q(student_id__icontains=search) |
                Q(email__icontains=search) |
                Q(department__icontains=search)
            )
        if department:
            students = students.filter(department__icontains=department)
        if year:
            students = students.filter(year=year)
    
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_students': students.count(),
    }
    return render(request, 'students/student_list.html', context)


@login_required
@admin_required
def student_create(request):
    """Create new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            # Update room occupancy if room is assigned
            if student.room:
                student.room.update_occupancy()
            messages.success(request, f'Student {student.name} created successfully!')
            return redirect('students:list')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'button_text': 'Create Student'
    })


@login_required
@admin_required
def student_update(request, pk):
    """Update existing student"""
    student = get_object_or_404(Student, pk=pk)
    old_room = student.room
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            # Update room occupancy for both old and new rooms
            if old_room and old_room != student.room:
                old_room.update_occupancy()
            if student.room:
                student.room.update_occupancy()
            messages.success(request, f'Student {student.name} updated successfully!')
            return redirect('students:detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Edit Student: {student.name}',
        'button_text': 'Update Student'
    })


@login_required
def student_detail(request, pk):
    """View student details"""
    student = get_object_or_404(Student, pk=pk)
    
    # Students can only view their own profile
    if request.user.is_student_user:
        if not hasattr(request.user, 'student_profile') or request.user.student_profile.pk != pk:
            messages.error(request, 'You can only view your own profile.')
            return redirect('dashboard:index')
    
    context = {
        'student': student,
        'attendance_percentage': student.get_attendance_percentage(),
        'pending_fees': student.get_pending_fees(),
    }
    return render(request, 'students/student_detail.html', context)


@login_required
@admin_required
def student_delete(request, pk):
    """Delete student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        room = student.room
        name = student.name
        student.delete()
        # Update room occupancy
        if room:
            room.update_occupancy()
        messages.success(request, f'Student {name} deleted successfully!')
        return redirect('students:list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})
