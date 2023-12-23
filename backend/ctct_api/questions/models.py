# backend/ctct_api/questions/models.py
from django.db import models
import datetime

# Model for an academic week
class Week(models.Model):
    number = models.IntegerField(unique=True)
    theme = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    description = models.TextField(default="No description provided.")
    
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

class Question(models.Model):
    # Types of questions supported
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False'),
        ('L', 'Likert Scale'),
    )
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    activity = models.ForeignKey(Activity, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Question ID {self.id} - {self.question_text}"

class Option(models.Model):
    # Each option is linked to a specific question
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for Question ID {self.question.id}: {self.option_text} - {'Correct' if self.is_correct else 'Incorrect'}"

class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Using through to define an additional model for ordering questions in a questionnaire
    questions = models.ManyToManyField(Question, through='QuestionnaireQuestion')
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)
    def get_ordered_questions(self):
        return [qq.question for qq in self.questionnairequestion_set.all().order_by('order')]
    def __str__(self):
        return f"Questionnaire: {self.title}"

class QuestionnaireQuestion(models.Model):
    # Intermediate model to define the order of questions in a questionnaire
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['questionnaire', 'question']

    def __str__(self):
        return f"Question {self.order} in {self.questionnaire.title}"

# Model for an answer to a question
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    # Allow nulls for selected_option if an answer hasn't been selected yet
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # Handle the possibility of selected_option being None
        selected_option_text = self.selected_option.option_text if self.selected_option else "No answer selected"
        return f"Answer by {self.student.user.get_full_name()} for {self.question.question_text}: {selected_option_text}"

# Model for tracking activity attempts by students
class ActivityAttempt(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, verbose_name=("Student"))
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name=("Activity"))
    start_time = models.DateTimeField(verbose_name=("Start Time"))
    end_time = models.DateTimeField(verbose_name=("End Time"))
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=("Score"))

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.activity.title} Attempt"

    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()

    class Meta:
        verbose_name = ("Activity Attempt")
        verbose_name_plural = ("Activity Attempts")

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
