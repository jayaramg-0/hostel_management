from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Room
from .forms import RoomForm, RoomAllocationForm
from accounts.decorators import admin_required


@login_required
@admin_required
def room_list(request):
    """List all rooms with search and pagination"""
    rooms = Room.objects.all()
    
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    floor = request.GET.get('floor', '')
    
    if search:
        rooms = rooms.filter(room_number__icontains=search)
    if status:
        rooms = rooms.filter(status=status)
    if floor:
        rooms = rooms.filter(floor=floor)
    
    # Get unique floors for filter dropdown
    floors = Room.objects.values_list('floor', flat=True).distinct().order_by('floor')
    
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'floor': floor,
        'floors': floors,
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(status='available').count(),
        'full_rooms': Room.objects.filter(status='full').count(),
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
@admin_required
def room_create(request):
    """Create new room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room {room.room_number} created successfully!')
            return redirect('rooms:list')
    else:
        form = RoomForm()
    
    return render(request, 'rooms/room_form.html', {
        'form': form,
        'title': 'Add New Room',
        'button_text': 'Create Room'
    })


@login_required
@admin_required
def room_update(request, pk):
    """Update existing room"""
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room {room.room_number} updated successfully!')
            return redirect('rooms:detail', pk=room.pk)
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'rooms/room_form.html', {
        'form': form,
        'room': room,
        'title': f'Edit Room: {room.room_number}',
        'button_text': 'Update Room'
    })


@login_required
def room_detail(request, pk):
    """View room details"""
    room = get_object_or_404(Room, pk=pk)
    students = room.students.filter(is_active=True)
    
    context = {
        'room': room,
        'students': students,
    }
    return render(request, 'rooms/room_detail.html', context)


@login_required
@admin_required
def room_delete(request, pk):
    """Delete room"""
    room = get_object_or_404(Room, pk=pk)
    
    # Check if room has students
    if room.students.filter(is_active=True).exists():
        messages.error(request, 'Cannot delete room with assigned students. Please vacate the room first.')
        return redirect('rooms:detail', pk=room.pk)
    
    if request.method == 'POST':
        room_number = room.room_number
        room.delete()
        messages.success(request, f'Room {room_number} deleted successfully!')
        return redirect('rooms:list')
    
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})


@login_required
@admin_required
def room_allocate(request, pk):
    """Allocate student to room"""
    room = get_object_or_404(Room, pk=pk)
    
    if room.status == 'full':
        messages.error(request, 'This room is full. Cannot allocate more students.')
        return redirect('rooms:detail', pk=room.pk)
    
    if request.method == 'POST':
        form = RoomAllocationForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            student.room = room
            student.save()
            room.update_occupancy()
            messages.success(request, f'{student.name} allocated to Room {room.room_number} successfully!')
            return redirect('rooms:detail', pk=room.pk)
    else:
        form = RoomAllocationForm()
    
    return render(request, 'rooms/room_allocate.html', {
        'form': form,
        'room': room,
    })


@login_required
@admin_required
def room_vacate(request, pk, student_pk):
    """Vacate student from room"""
    room = get_object_or_404(Room, pk=pk)
    from students.models import Student
    student = get_object_or_404(Student, pk=student_pk)
    
    if student.room != room:
        messages.error(request, 'Student is not assigned to this room.')
        return redirect('rooms:detail', pk=room.pk)
    
    if request.method == 'POST':
        student.room = None
        student.save()
        room.update_occupancy()
        messages.success(request, f'{student.name} vacated from Room {room.room_number} successfully!')
        return redirect('rooms:detail', pk=room.pk)
    
    return render(request, 'rooms/room_vacate_confirm.html', {
        'room': room,
        'student': student,
    })
