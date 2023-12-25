
# backend/ctct_api/questions/serializers.py

# Import necessary modules and models
from rest_framework import serializers
from .models import (Activity, Week, ActivityParticipation, ActivityAttempt,
                     FileSubmission, DownloadableContent, QuestionnaireQuestion,
                     Question, Option, Questionnaire, Answer, 
                     QuestionResponseDetail, StudentQuestionnaireResponse)
from users.serializers import TeacherProfileSerializer, StudentProfileSerializer

# Serializer for the Week model
class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'number', 'theme']

# Serializer for the Activity model with nested data
class ActivitySerializer(serializers.ModelSerializer):
    # Using slug fields for readable representations of related objects
    classroom = serializers.SlugRelatedField(slug_field="name", read_only=True)
    teacher = TeacherProfileSerializer(read_only=True)
    week = serializers.SlugRelatedField(slug_field="theme", read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

# Serializer for the ActivityAttempt model
class ActivityAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAttempt
        fields = ['id', 'student', 'activity', 'start_time', 'end_time', 'score']

# Serializer for the ActivityParticipation model
class ActivityParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipation
        fields = ['id', 'student', 'activity', 'response']

# Serializer for the FileSubmission model with nested activity and student data
class FileSubmissionSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)

    class Meta:
        model = FileSubmission
        fields = ['id', 'activity', 'student', 'submitted_file', 'timestamp']

# Serializer for the DownloadableContent model with nested week data
class DownloadableContentSerializer(serializers.ModelSerializer):
    week = serializers.SlugRelatedField(slug_field="theme", read_only=True)

    class Meta:
        model = DownloadableContent
        fields = ['id', 'title', 'week', 'file', 'uploaded_at']

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
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'description', 'activity', 'questions']

    def get_questions(self, obj):
        # Return a list of question IDs associated with the questionnaire
        return obj.questions.values_list('id', flat=True)

# Serializer for the Answer model
class AnswerSerializer(serializers.ModelSerializer):
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
        return instance

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
    response_details = QuestionResponseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = StudentQuestionnaireResponse
        fields = ['student', 'questionnaire', 'answered_on', 'response_details']
        read_only_fields = ['answered_on']
