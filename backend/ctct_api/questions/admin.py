from django.contrib import admin
from .models import (Week, Activity, ActivityAttempt, ActivityParticipation, 
                     FileSubmission, DownloadableContent,
                     Question, Questionnaire, Answer, Option)


admin.site.register(Week)
admin.site.register(Activity)
admin.site.register(ActivityAttempt)
admin.site.register(ActivityParticipation)
admin.site.register(FileSubmission)
admin.site.register(DownloadableContent)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Questionnaire)
admin.site.register(Answer)