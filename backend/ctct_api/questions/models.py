# backend/ctct_api/questions/models.py
from django.db import models
import datetime

# Model representing academic weeks
class Week(models.Model):
    number = models.IntegerField(unique=True)
    theme = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today)  
    end_date = models.DateField(default=datetime.date.today)   
    description = models.TextField(default="Sem descrição fornecida.")
    
    def __str__(self):
        return f"Week {self.number}: {self.theme}"

# Model for various activities like quizzes, questions, etc.
class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    classroom = models.ForeignKey('users.Classroom', on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Model for tracking activity participation by students
class ActivityParticipation(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Participação de {self.student.user.get_full_name()} em {self.activity.title}"

# Model for handling file submissions by students
class FileSubmission(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='activity_submissions/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submissão de {self.student.user.get_full_name()} para {self.activity.title}"

# Model for downloadable content available to students
class DownloadableContent(models.Model):
    title = models.CharField(max_length=255)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    file = models.FileField(upload_to='downloadable_content/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conteúdo: {self.title} (Semana {self.week.number})"
