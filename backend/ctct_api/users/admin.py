from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import (User, StudentProfile, TeacherProfile, Course, Classroom, StudentGroup, TPRegistration)

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher')}),
    )

admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(StudentGroup)
admin.site.register(TPRegistration)