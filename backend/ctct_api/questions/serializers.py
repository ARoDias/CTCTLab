
# backend/ctct_api/questions/serializers.py

# Import necessary modules and models
from rest_framework import serializers
#from django.shortcuts import get_object_or_404
from .models import (Activity, Week, #ActivityParticipation, ActivityAttempt, 
                     # FileSubmission, DownloadableContent, 
                     QuestionnaireQuestion,
                     Question, Option, Questionnaire, #Answer, 
                     QuestionResponseDetail, StudentQuestionnaireResponse, ActivityInstance)
#from users.serializers import TeacherProfileSerializer, StudentProfileSerializer
from users.models import StudentProfile, Classroom
# Serializer for the Week model
class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'number', 'theme']

# Serializer for the Activity model with nested data
class ActivitySerializer(serializers.ModelSerializer):
    # Assuming new fields in the Activity model
    # Update with actual field names and logic as per new model structure

    class Meta:
        model = Activity
        fields = '__all__'

class ActivityInstanceSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=True)

    class Meta:
        model = ActivityInstance
        fields = ['id', 'activity', 'classrooms', 'start_time', 'end_time', 'is_active']

    def create(self, validated_data):
        classrooms = validated_data.pop('classrooms')
        activity_instance = ActivityInstance.objects.create(**validated_data)
        activity_instance.classrooms.set(classrooms)
        return activity_instance

    def update(self, instance, validated_data):
        if 'classrooms' in validated_data:
            classrooms = validated_data.pop('classrooms')
            instance.classrooms.set(classrooms)
        return super().update(instance, validated_data)

# Serializer for the ActivityAttempt model
# class ActivityAttemptSerializer(serializers.ModelSerializer):
#     activity_instance = serializers.PrimaryKeyRelatedField(
#         queryset=ActivityInstance.objects.all(),
#         source='activity_instance'
#     )
#
#     class Meta:
#         model = ActivityAttempt
#         fields = ['id', 'student', 'activity_instance', 'start_time', 'end_time', 'score']


# Serializer for the ActivityParticipation model
# class ActivityParticipationSerializer(serializers.ModelSerializer):
#     activity_instance = serializers.PrimaryKeyRelatedField(
#         queryset=ActivityInstance.objects.all(),
#         source='activity_instance'
#     )
#
#     class Meta:
#         model = ActivityParticipation
#         fields = ['id', 'student', 'activity_instance', 'response']

# Serializer for the FileSubmission model with nested activity and student data
# class FileSubmissionSerializer(serializers.ModelSerializer):
#     activity_instance = ActivityInstanceSerializer(read_only=True)
#     student = StudentProfileSerializer(read_only=True)
#
#     class Meta:
#         model = FileSubmission
#         fields = ['id', 'activity_instance', 'student', 'submitted_file', 'timestamp']


# Serializer for the DownloadableContent model with nested week data
""" class DownloadableContentSerializer(serializers.ModelSerializer):
    week = serializers.SlugRelatedField(slug_field="theme", read_only=True)

    class Meta:
        model = DownloadableContent
        fields = ['id', 'title', 'week', 'file', 'uploaded_at'] """

# Serializer for the Option model
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

# Serializer for the Question model including related options
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

# Serializer for the Questionnaire model
class QuestionnaireSerializer(serializers.ModelSerializer):
    week = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'description', 'activity', 'questions', 'week', 'is_active']

    def get_week(self, obj):
        return obj.activity.week.number if obj.activity.week else None

    def get_is_active(self, obj):
        activity_instances = ActivityInstance.objects.filter(activity=obj.activity)
        return any(instance.is_active for instance in activity_instances)


# Serializer for the Answer model
""" class AnswerSerializer(serializers.ModelSerializer):
    is_correct = serializers.ReadOnlyField()  # Ensure this field is read-only

    class Meta:
        model = Answer
        fields = ['id', 'question', 'student', 'selected_option', 'is_correct']

    # Custom create method to set is_correct based on the selected option
    def create(self, validated_data):
        selected_option = validated_data.get('selected_option')
        is_correct = selected_option.is_correct if selected_option else False
        answer = Answer.objects.create(**validated_data, is_correct=is_correct)
        return answer

    # Custom update method to handle updates to the selected option
    def update(self, instance, validated_data):
        selected_option = validated_data.get('selected_option')
        if selected_option:
            instance.selected_option = selected_option
            instance.is_correct = selected_option.is_correct
        instance.save()
        return instance """

# Serializer for the QuestionnaireQuestion model
class QuestionnaireQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireQuestion
        fields = ['id', 'questionnaire', 'question', 'order']

# Serializer for the QuestionResponseDetail model
class QuestionResponseDetailSerializer(serializers.ModelSerializer):
    # Use a PrimaryKeyRelatedField for selected_option to allow POSTing the option ID
    selected_option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all())

    class Meta:
        model = QuestionResponseDetail
        fields = ['student_response', 'question', 'selected_option', 'is_correct']
        read_only_fields = ['is_correct']

    def create(self, validated_data):
        # Ensure the selected option belongs to the question
        question = validated_data.get('question')
        selected_option = validated_data.get('selected_option')
        if selected_option.question != question:
            raise serializers.ValidationError("The selected option does not belong to the specified question.")
        
        # Set is_correct based on the selected option's correctness
        validated_data['is_correct'] = selected_option.is_correct
        return QuestionResponseDetail.objects.create(**validated_data)



# Serializer for the StudentQuestionnaireResponse model
class StudentQuestionnaireResponseSerializer(serializers.ModelSerializer):
    student_number = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentQuestionnaireResponse
        fields = ['student', 'questionnaire', 'answered_on', 'response_details', 'student_number']
        read_only_fields = ['answered_on', 'response_details', 'student']

    def create(self, validated_data):
        student_number = validated_data.pop('student_number', None)
        try:
            student_profile = StudentProfile.objects.get(student_number=student_number)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError({"student_number": "Invalid student number."})

        validated_data['student'] = student_profile

        # Check if a response already exists for this student and questionnaire
        questionnaire = validated_data.get('questionnaire')
        response, created = StudentQuestionnaireResponse.objects.get_or_create(
            student=student_profile, 
            questionnaire=questionnaire,
            defaults=validated_data
        )

        if not created:
            for attr, value in validated_data.items():
                setattr(response, attr, value)
            response.save()

        return response



    def update(self, instance, validated_data):
        """
        Update a StudentQuestionnaireResponse instance.
        """
        # No change needed here; if 'student' is in validated_data, it already contains the StudentProfile instance
        return super().update(instance, validated_data)
    
class QuestionStatsSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    incorrect_count = serializers.IntegerField()

    @staticmethod
    def get_question_stats(question_id):
        correct_count = QuestionResponseDetail.objects.filter(
            question_id=question_id, is_correct=True
        ).count()
        incorrect_count = QuestionResponseDetail.objects.filter(
            question_id=question_id, is_correct=False
        ).count()
        return {
            "question_id": question_id,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count
        }

class OptionDistributionSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    count = serializers.IntegerField()

    @staticmethod
    def get_option_distribution(question_id):
        distribution = []
        options = Option.objects.filter(question_id=question_id)
        for option in options:
            count = QuestionResponseDetail.objects.filter(question=question_id, selected_option=option).count()
            distribution.append({
                'option_id': option.id,
                'count': count
            })
        return distribution

class DetailedQuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options']

class DetailedQuestionnaireSerializer(serializers.ModelSerializer):
    questions = DetailedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'description', 'questions']

