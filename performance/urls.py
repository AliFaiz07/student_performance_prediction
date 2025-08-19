# performance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student-register/', views.student_register, name='student_register'),
    path('student-login/', views.student_login, name='student_login'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),

    path('add/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('export/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
