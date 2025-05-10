from django.db import models, IntegrityError, OperationalError
from django.core.exceptions import ValidationError
from abc import ABCMeta, ABC, abstractmethod
import datetime
import re

# Abstract base class using abstraction
class CustomModelMeta(ABCMeta, type(models.Model)):
    pass

# Now you can safely define your abstract base model like this:
class Person(models.Model, ABC, metaclass=CustomModelMeta):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method.")


# Custom exception for application logic
class CourseNotFoundError(Exception):
    def __init__(self, course):
        super().__init__(f"The course '{course}' is not offered.")


# Inheritance from Person, implements abstraction
class Student(Person):
    app_id = models.CharField(max_length=20, unique=True, )
    year_of_passing = models.IntegerField()

    COURSE_CHOICES = [
        ('BBA', 'BBA'),
        ('BTech', 'BTech'),
        ('MBA', 'MBA'),
        ('Design', 'Design'),
    ]
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.app_id})"

    def get_role(self):  # Polymorphism - implementation of abstract method
        return "Student"

    def is_graduating(self):
        """Encapsulation: internal graduation logic"""
        current_year = datetime.datetime.now().year
        return self.year_of_passing <= current_year

    @classmethod
    def get_students_by_course(cls, course_name):
        """Class method to filter students by course"""
        if course_name not in dict(cls.COURSE_CHOICES):
            raise CourseNotFoundError(course_name)
        return cls.objects.filter(course=course_name)


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.status}"

    def get_role(self):  # Polymorphism example again
        return "Attendance Record"

    @staticmethod
    def get_attendance_status_color(status):
        """Static method to return color based on attendance status"""
        color_map = {
            'Present': 'green',
            'Absent': 'red',
            'Late': 'orange',
        }
        return color_map.get(status, 'black')


# Validator for app_id
def validate_app_id(value):
    if not re.match(r'^\d{7}$', str(value)):
        raise ValidationError('App ID must be exactly 7 digits.')


# Exception handling - safe database operations
def add_student(name, app_id, year_of_passing, course):
    try:
        student = Student.objects.create(
            name=name,
            app_id=app_id,
            year_of_passing=year_of_passing,
            course=course
        )
        return student
    except ValidationError as e:
        print(f"Validation Error: {e}")
    except IntegrityError:
        print("Error: Duplicate App ID. This App ID already exists.")
    except OperationalError:
        print("Database Connection Error. Please check your MySQL setup.")
    except CourseNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Create your models here.
