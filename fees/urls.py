from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fee_list, name='list'),
    path('create/', views.fee_create, name='create'),
    path('<int:pk>/', views.fee_detail, name='detail'),
    path('<int:pk>/edit/', views.fee_update, name='update'),
    path('<int:pk>/delete/', views.fee_delete, name='delete'),
    path('<int:pk>/payment/', views.fee_update_payment, name='update_payment'),
    path('student/<int:pk>/', views.student_fees, name='student_fees'),
]
