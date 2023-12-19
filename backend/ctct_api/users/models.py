# backend/ctct_api/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Custom User Model with student and teacher flags
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)

# Course model with a unique name
class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# Classroom model with optional capacity attribute
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# Extended student profile with additional attributes
class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True}, verbose_name=_("User"))
    tp_classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, related_name='tp_students')
    student_number = models.IntegerField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, verbose_name=_("Age"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    data_consent = models.BooleanField(default=False, verbose_name=_("Data Consent"))

    def __str__(self):
        return f"{self.student_number} - {self.user.get_full_name()}"

# Teacher profile with user one-to-one relationship and classroom many-to-many relationship
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classrooms = models.ManyToManyField(Classroom)

    def __str__(self):
        return self.user.get_full_name()

# TP class registration model with student foreign key and classroom foreign key
class TPRegistration(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    session_time = models.CharField(max_length=100)

    def __str__(self):
        return f"Inscrição de {self.student.user.get_full_name()} na Sala {self.classroom.name}"

# Student group model with many-to-many relationship to StudentProfile and foreign key to Classroom and Week
class StudentGroup(models.Model):
    students = models.ManyToManyField(StudentProfile)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    week = models.ForeignKey('questions.Week', on_delete=models.CASCADE)

    def __str__(self):
        return f"Grupo da Sala {self.classroom.name} (Semana {self.week.number})"
