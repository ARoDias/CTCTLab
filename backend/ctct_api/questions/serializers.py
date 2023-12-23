
# backend/ctct_api/questions/serializers.py
from rest_framework import serializers
from .models import (Activity, Week, ActivityParticipation, ActivityAttempt,
                     FileSubmission, DownloadableContent, 
                     Question, Option, Questionnaire, Answer)
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
        fields = '__all__'

# Serializer for ActivityAttempt
class ActivityAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAttempt
        fields = ['id', 'student', 'activity', 'start_time', 'end_time', 'score']


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

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

class QuestionnaireSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'description', 'questions']

    def get_questions(self, obj):
        questions = obj.get_ordered_questions()
        return QuestionSerializer(questions, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    class Meta:
        model = Answer
        fields = '__all__'
