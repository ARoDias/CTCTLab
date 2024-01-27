# questions/admin.py
# Import necessary modules and models
from django.contrib import admin
from .models import (Week, Activity, #ActivityAttempt, ActivityParticipation, FileSubmission, DownloadableContent, 
                     QuestionnaireQuestion, Question, Questionnaire, Option, #Answer,S
                     ActivityInstance, StudentQuestionnaireResponse, QuestionResponseDetail)

class QuestionResponseDetailAdmin(admin.ModelAdmin):
    # Especifica os campos que devem ser somente leitura
    readonly_fields = ('is_correct',)

    # Configurações adicionais, se necessário
    list_display = ('question', 'student_response', 'is_correct')
    list_filter = ('is_correct', 'question')

# Register models for admin site
admin.site.register(Week)
admin.site.register(Activity)
admin.site.register(ActivityInstance)
#admin.site.register(ActivityAttempt)
#admin.site.register(ActivityParticipation)
#admin.site.register(FileSubmission)
#admin.site.register(DownloadableContent)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireQuestion)
#admin.site.register(Answer)
admin.site.register(StudentQuestionnaireResponse) 
admin.site.register(QuestionResponseDetail, QuestionResponseDetailAdmin)