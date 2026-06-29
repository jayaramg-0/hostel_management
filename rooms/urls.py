from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='list'),
    path('create/', views.room_create, name='create'),
    path('<int:pk>/', views.room_detail, name='detail'),
    path('<int:pk>/edit/', views.room_update, name='update'),
    path('<int:pk>/delete/', views.room_delete, name='delete'),
    path('<int:pk>/allocate/', views.room_allocate, name='allocate'),
    path('<int:pk>/vacate/<int:student_pk>/', views.room_vacate, name='vacate'),
]
