from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin_user:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    return wrapper


def student_required(view_func):
    """Decorator to check if user is student"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student_user:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'This page is only for students.')
        return redirect('dashboard:index')
    return wrapper
