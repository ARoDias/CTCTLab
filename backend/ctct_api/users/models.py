# backend/ctct_api/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Custom User Model
class User(AbstractUser):
    # Flags to identify if the user is a student or a teacher
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)

# Model representing a course
class Course(models.Model):
    # Name of the course, must be unique
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# Model representing a classroom
class Classroom(models.Model):
    # Classroom name
    name = models.CharField(max_length=100)
    # Maximum capacity of the classroom, can be blank or null
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# Extended model for Student with additional attributes
class StudentProfile(models.Model):
    # Gender choices for the student
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    
    # One-to-one relationship with User model, only for students
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True}, verbose_name=_("User"))
    # Foreign key to the Classroom model, related to TP classes
    tp_classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, related_name='tp_students')
    # Unique student number
    student_number = models.IntegerField(unique=True)
    # Foreign key to the Course model
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Age of the student, default is 18
    age = models.IntegerField(default=18, verbose_name=_("Age"))
    # Gender of the student
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    # Consent for data usage, default is False
    data_consent = models.BooleanField(default=False, verbose_name=_("Data Consent"))

    def __str__(self):
        return f"{self.student_number} - {self.user.get_full_name()}"

# Extended model for Teacher with related fields
class TeacherProfile(models.Model):
    # One-to-one relationship with User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Many-to-many relationship with Classroom model
    classrooms = models.ManyToManyField(Classroom)

    def __str__(self):
        return self.user.get_full_name()
    
# Model for student registration to Theorical-Practical (TP) classes
class TPRegistration(models.Model):
    # Foreign key to the StudentProfile model
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    # Foreign key to the Classroom model
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    # Time of the TP session, could also be a DateTimeField
    session_time = models.CharField(max_length=100)

    def __str__(self):
        return f"Inscrição de {self.student.user.get_full_name()} na Sala {self.classroom.name}"

# Model for student groups
class StudentGroup(models.Model):
    # Many-to-many relationship with StudentProfile model
    students = models.ManyToManyField(StudentProfile)
    # Foreign key to the Classroom model
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    # Foreign key to the Week model
    week = models.ForeignKey('questions.Week', on_delete=models.CASCADE)

    def __str__(self):
        return f"Grupo da Sala {self.classroom.name} (Semana {self.week.number})"