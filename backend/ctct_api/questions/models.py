# backend/ctct_api/questions/models.py
from django.db import models
import datetime
from django.core.exceptions import ValidationError

class Week(models.Model):
    # Unique identifier for each academic week, indexed for efficient querying
    number = models.IntegerField(unique=True, db_index=True)
    theme = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    description = models.TextField(default="No description provided.")

    def __str__(self):
        return f"Week {self.number}: {self.theme}"

# Updated Activity model
class Activity(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# ActivityInstance model
class ActivityInstance(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    classrooms = models.ManyToManyField('users.Classroom')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity.title} in {', '.join(classroom.name for classroom in self.classrooms.all())}"

class Questionnaire(models.Model):
    # Title of the questionnaire, indexed for efficient searching
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    questions = models.ManyToManyField('Question', through='QuestionnaireQuestion', related_name='questionnaires')
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)

    def get_ordered_questions(self):
        # Retrieves questions in the order specified in the through model
        return [qq.question for qq in self.questionnairequestion_set.all().order_by('order')]

    def __str__(self):
        return f"Questionnaire: {self.title}"

class Question(models.Model):
    # Defines question types (e.g., MCQ, True/False, Likert Scale)
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice Question'),
        ('TF', 'True/False'),
        ('L', 'Likert Scale'),
    )
    question_text = models.CharField(max_length=255, db_index=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE, related_name='questions_in_questionnaire', null=True)

    def __str__(self):
        return f"Question ID {self.id} - {self.question_text}"

class Option(models.Model):
    # Each option is linked to a specific question
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for Question ID {self.question.id}: {self.option_text} - {'Correct' if self.is_correct else 'Incorrect'}"

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

""" class Answer(models.Model):
    # Stores a student's answer to a question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        selected_option_text = self.selected_option.option_text if self.selected_option else "No answer selected"
        return f"Answer by {self.student.user.get_full_name()} for {self.question.question_text}: {selected_option_text}" """

""" class ActivityAttempt(models.Model):
    # Tracks an attempt by a student to complete an activity
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, verbose_name=("Student"))
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name=("Activity"))
    start_time = models.DateTimeField(verbose_name=("Start Time"))
    end_time = models.DateTimeField(verbose_name=("End Time"))
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=("Score"))

    @property
    def duration(self):
        # Calculates the duration of the activity attempt
        return (self.end_time - self.start_time).total_seconds()

    class Meta:
        verbose_name = ("Activity Attempt")
        verbose_name_plural = ("Activity Attempts")

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.activity.title} Attempt"

class ActivityParticipation(models.Model):
    # Records a student's participation in an activity
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Participação de {self.student.user.get_full_name()} em {self.activity.title}"

class FileSubmission(models.Model):
    # Tracks file submissions by students for activities
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='activity_submissions/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submissão de {self.student.user.get_full_name()} para {self.activity.title}"

class DownloadableContent(models.Model):
    # Represents downloadable content associated with a week of the academic calendar
    title = models.CharField(max_length=255, db_index=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    file = models.FileField(upload_to='downloadable_content/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conteúdo: {self.title} (Semana {self.week.number})" """

class StudentQuestionnaireResponse(models.Model):
    """
    Model to record a student's overall response to a questionnaire.
    Links to a student profile and the questionnaire they responded to.
    """
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answered_on = models.DateTimeField(auto_now_add=True)  # Automatically set the time when the response is created

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.questionnaire.title} Response"
    
    class Meta:
        unique_together = ['student', 'questionnaire']
        verbose_name = ("Student Questionnaire Response")
        verbose_name_plural = ("Student Questionnaire Responses")

class QuestionResponseDetail(models.Model):
    """
    Model to store detailed responses of a student to each question in a questionnaire.
    Links to the StudentQuestionnaireResponse and records the selected option and its correctness.
    Ensures that the selected option belongs to the question being answered.
    """
    student_response = models.ForeignKey(
        StudentQuestionnaireResponse, related_name='response_details', on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # Set based on the selected option's correctness

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure that the selected option belongs to the question.
        Also, automatically set the is_correct field based on the selected option.
        """
        if self.selected_option and self.selected_option.question != self.question:
            raise ValidationError("Selected option does not belong to the question")
        
        self.is_correct = self.selected_option.is_correct if self.selected_option else False
        super(QuestionResponseDetail, self).save(*args, **kwargs)

    def __str__(self):
        correct_text = 'Correct' if self.is_correct else 'Incorrect'
        return f"Response to Question ID {self.question.id} - {correct_text}"

    class Meta:
        unique_together = ['student_response', 'question']
        verbose_name = "Question Response Detail"
        verbose_name_plural = "Question Response Details"