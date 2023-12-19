from django.contrib import admin
from .models import (Week, Activity, ActivityParticipation, FileSubmission, DownloadableContent)


admin.site.register(Week)
admin.site.register(Activity)
admin.site.register(ActivityParticipation)
admin.site.register(FileSubmission)
admin.site.register(DownloadableContent)

