from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/', views.mark_attendance, name='mark'),
    path('report/', views.attendance_report, name='report'),
    path('student/<int:pk>/', views.student_attendance, name='student'),
]
