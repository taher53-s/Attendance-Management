from django.urls import path
from . import views

app_name = 'attendance'  # Namespace for reversing URLs

urlpatterns = [
    path('', views.home, name='home'),
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_report/', views.attendance_report, name='attendance_report'),
    path('student/<int:student_id>/', views.student_details, name='student_details'),  # NEW: Student details route
    path('students/', views.student_list, name='student_list'),  # Optional: to separately show all students
]
