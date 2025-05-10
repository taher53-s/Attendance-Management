from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentEnrollmentForm, AttendanceForm
from .models import Student, AttendanceRecord, add_student, CourseNotFoundError
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

def home(request):
    """Render the home page."""
    return render(request, 'home.html')


def enroll_student(request):
    """Handles student enrollment with form validation and exception handling."""
    try:
        if request.method == 'POST':
            form = StudentEnrollmentForm(request.POST)
            if form.is_valid():
                # Using model method for encapsulated exception-safe creation
                student = form.save(commit=False)
                student.save()
                return redirect('attendance:enroll_student')
        else:
            form = StudentEnrollmentForm()

        students = Student.objects.all()
        return render(request, 'attendance/enroll_student.html', {'form': form, 'students': students})

    except IntegrityError:
        return render(request, 'error.html', {'message': 'Duplicate entry detected!'})
    except ValidationError as e:
        return render(request, 'error.html', {'message': str(e)})
    except CourseNotFoundError as e:
        return render(request, 'error.html', {'message': str(e)})
    except Exception as e:
        return render(request, 'error.html', {'message': f"An unexpected error occurred: {str(e)}"})


def student_list(request):
    """Displays a list of all enrolled students."""
    try:
        students = Student.objects.all()
        return render(request, 'attendance/enroll_student.html', {'students': students})
    except Exception as e:
        return render(request, 'error.html', {'message': f"Could not fetch students: {str(e)}"})


def mark_attendance(request):
    """Handles marking attendance with form validation and query handling."""
    try:
        if request.method == 'POST':
            form = AttendanceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('attendance:mark_attendance')
        else:
            form = AttendanceForm()

        attendance_list = AttendanceRecord.objects.all()
        return render(request, 'attendance/mark_attendance.html', {'form': form, 'attendance_list': attendance_list})

    except Exception as e:
        return render(request, 'error.html', {'message': f"An error occurred while marking attendance: {str(e)}"})


def attendance_report(request):
    """Generates an attendance report with student attendance statistics."""
    try:
        total_students = Student.objects.count()
        attendance_records = AttendanceRecord.objects.all()
        present_count = attendance_records.filter(status='Present').count()
        absent_count = attendance_records.filter(status='Absent').count()
        late_count = attendance_records.filter(status='Late').count()

        context = {
            'total_students': total_students,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
        }
        return render(request, 'attendance/attendance_report.html', context)

    except Exception as e:
        return render(request, 'error.html', {'message': f"Error generating attendance report: {str(e)}"})


def student_details(request, student_id):
    """Displays details of a specific student."""
    try:
        student = get_object_or_404(Student, id=student_id)
        is_graduating = student.is_graduating()  # Calls encapsulated logic
        return render(request, 'attendance/student_details.html', {
            'student': student,
            'is_graduating': is_graduating,
            'role': student.get_role(),  # Polymorphism in action
        })
    except Exception as e:
        return render(request, 'error.html', {'message': f"Could not retrieve student details: {str(e)}"})

  # You need to create this template
