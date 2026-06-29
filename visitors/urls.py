from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('', views.visitor_list, name='list'),
    path('register/', views.visitor_create, name='create'),
    path('<int:pk>/', views.visitor_detail, name='detail'),
    path('<int:pk>/checkout/', views.visitor_checkout, name='checkout'),
    path('history/<int:student_pk>/', views.visitor_history, name='history'),
]
