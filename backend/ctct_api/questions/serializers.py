
# backend/ctct_api/questions/serializers.py
from rest_framework import serializers
from .models import (Activity, Week, ActivityParticipation, FileSubmission, DownloadableContent)
from users.serializers import TeacherProfileSerializer, StudentProfileSerializer

# Week Model Serializer
class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'number', 'theme']

# Activity Model Serializer with Nested Classroom, Teacher, and Week Data
class ActivitySerializer(serializers.ModelSerializer):
    classroom = serializers.SlugRelatedField(slug_field="name", read_only=True)
    teacher = TeacherProfileSerializer(read_only=True)
    week = serializers.SlugRelatedField(slug_field="theme", read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'classroom', 'teacher', 'week', 'is_active']


# Activity Participation Model Serializer
class ActivityParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipation
        fields = ['id', 'student', 'activity', 'response']

# File Submission Model Serializer with Nested Activity and Student Data
class FileSubmissionSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = FileSubmission
        fields = ['id', 'activity', 'student', 'submitted_file', 'timestamp']

# Downloadable Content Model Serializer with Nested Week Data
class DownloadableContentSerializer(serializers.ModelSerializer):
    week = serializers.SlugRelatedField(slug_field="theme", read_only=True)

    class Meta:
        model = DownloadableContent
        fields = ['id', 'title', 'week', 'file', 'uploaded_at']


# Redefining Activity Serializer for All Fields
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

