# questions/admin.py
# Import necessary modules and models
from django.contrib import admin
from .models import (Week, Activity, ActivityAttempt, ActivityParticipation, 
                     FileSubmission, DownloadableContent, QuestionnaireQuestion,
                     Question, Questionnaire, Answer, Option, 
                     StudentQuestionnaireResponse, QuestionResponseDetail)

# Register models for admin site
admin.site.register(Week)
admin.site.register(Activity)
admin.site.register(ActivityAttempt)
admin.site.register(ActivityParticipation)
admin.site.register(FileSubmission)
admin.site.register(DownloadableContent)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireQuestion)
admin.site.register(Answer)
admin.site.register(StudentQuestionnaireResponse) 
admin.site.register(QuestionResponseDetail)
