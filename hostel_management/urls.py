"""
URL configuration for hostel_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('rooms/', include('rooms.urls')),
    path('attendance/', include('attendance.urls')),
    path('visitors/', include('visitors.urls')),
    path('complaints/', include('complaints.urls')),
    path('fees/', include('fees.urls')),
    path('notices/', include('notices.urls')),
    path('leave-requests/', include('leave_requests.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
