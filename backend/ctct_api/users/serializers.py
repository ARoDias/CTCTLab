
# backend/ctct_api/users/serializers.py
from rest_framework import serializers
from .models import (User, StudentProfile, TeacherProfile, Course, StudentGroup, Classroom)

# User Model Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_student', 'is_teacher']

# Student Profile Model Serializer with Nested User Data
class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tp_classroom = serializers.SlugRelatedField(slug_field="name", read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_number', 'course', 'age', 'gender', 'data_consent', 'tp_classroom']

# Teacher Profile Model Serializer with Nested User Data and Associated Classrooms
class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classrooms = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'classrooms']

# Course Model Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

# Student Group Model Serializer with Nested Student Profiles
class StudentGroupSerializer(serializers.ModelSerializer):
    students = StudentProfileSerializer(many=True, read_only=True)
    
    class Meta:
        model = StudentGroup
        fields = ['id', 'students', 'classroom', 'week']

# Custom Login Serializer
class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

# User and Student Profile Registration Serializer
class UserAndProfileRegistrationSerializer(serializers.Serializer):
    # Fields from User Model
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    
    # Fields from Student Profile Model
    course = serializers.SlugRelatedField(slug_field="name", queryset=Course.objects.all())
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=StudentProfile.GENDER_CHOICES)
    data_consent = serializers.BooleanField()
    
    def validate_username(self, value):
        """Check if the username is numeric."""
        if not value.isnumeric():
            raise serializers.ValidationError("The username must be numeric.")
        return value

    def create(self, validated_data):
    # Check for Unique Username
        if User.objects.filter(username=validated_data["username"]).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        
        user_data = {key: value for key, value in validated_data.items() if key in ['username', 'password', 'email', 'first_name', 'last_name']}
        
        # Assuming username is used as student_number
        profile_data = {key: value for key, value in validated_data.items() if key not in user_data}
        profile_data['student_number'] = validated_data['username']  # Set student_number explicitly
        
        # Create User Instance and Set Password
        user = User(**user_data)
        user.set_password(user_data["password"])
        user.is_active = False
        user.save()
        
        # Create Student Profile Linked to User
        StudentProfile.objects.create(user=user, **profile_data)

        return user

# Redefining Course Serializer for Id and Name Fields
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')

# Classroom Model Serializer
class ClassroomSerializer(serializers.ModelSerializer):
    class_type_display = serializers.CharField(source='get_class_type_display', read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'capacity', 'class_type', 'class_type_display']