from django.urls import path
from . import views

app_name = 'leave_requests'

urlpatterns = [
    path('', views.leave_list, name='list'),
    path('apply/', views.leave_create, name='create'),
    path('<int:pk>/', views.leave_detail, name='detail'),
    path('<int:pk>/approve/', views.leave_approve, name='approve'),
    path('<int:pk>/quick-approve/', views.leave_quick_approve, name='quick_approve'),
    path('<int:pk>/quick-reject/', views.leave_quick_reject, name='quick_reject'),
    path('history/<int:student_pk>/', views.leave_history, name='history'),
]
