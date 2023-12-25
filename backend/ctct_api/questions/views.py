# backend/ctct_api/questions/views.py

# Import necessary modules and classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import (Option, QuestionnaireQuestion, Activity, Week, FileSubmission, 
                     Question, Questionnaire, Answer, ActivityAttempt, 
                     StudentQuestionnaireResponse, QuestionResponseDetail)
from .serializers import (ActivitySerializer, ActivityAttemptSerializer, 
                          WeekSerializer, FileSubmissionSerializer, 
                          QuestionSerializer, QuestionnaireSerializer, 
                          AnswerSerializer, OptionSerializer, 
                          QuestionnaireQuestionSerializer, 
                          StudentQuestionnaireResponseSerializer, 
                          QuestionResponseDetailSerializer)
from rest_framework.decorators import api_view, permission_classes
from users.models import StudentGroup

# ViewSet for Activity model providing CRUD operations
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

# ViewSet for ActivityAttempt model providing CRUD operations
class ActivityAttemptViewSet(viewsets.ModelViewSet):
    queryset = ActivityAttempt.objects.all()
    serializer_class = ActivityAttemptSerializer

# ViewSet for Week model providing CRUD operations
class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

# ViewSet for FileSubmission model providing CRUD operations
class FileSubmissionViewSet(viewsets.ModelViewSet):
    queryset = FileSubmission.objects.all()
    serializer_class = FileSubmissionSerializer

# Custom view to return a list of activities related to the authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    if hasattr(request.user, 'studentprofile'):
        student_profile = request.user.studentprofile
        groups = StudentGroup.objects.filter(students=student_profile)
        activities = Activity.objects.filter(week__studentsgroup__in=groups, is_active=True)
    elif hasattr(request.user, 'teacherprofile'):
        teacher_profile = request.user.teacherprofile
        classrooms = teacher_profile.classrooms.all()
        activities = Activity.objects.filter(classroom__in=classrooms, is_active=True)
    else:
        activities = Activity.objects.none()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)

# ViewSet for Question model providing CRUD operations
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# ViewSet for Questionnaire model providing CRUD operations
class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

# ViewSet for Answer model providing CRUD operations
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

# ViewSet for Option model providing CRUD operations
class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

# ViewSet for QuestionnaireQuestion model providing CRUD operations
class QuestionnaireQuestionViewSet(viewsets.ModelViewSet):
    queryset = QuestionnaireQuestion.objects.all()
    serializer_class = QuestionnaireQuestionSerializer

# ViewSet for StudentQuestionnaireResponse model providing CRUD operations
class StudentQuestionnaireResponseViewSet(viewsets.ModelViewSet):
    queryset = StudentQuestionnaireResponse.objects.all()
    serializer_class = StudentQuestionnaireResponseSerializer

# ViewSet for QuestionResponseDetail model providing CRUD operations
class QuestionResponseDetailViewSet(viewsets.ModelViewSet):
    queryset = QuestionResponseDetail.objects.all()
    serializer_class = QuestionResponseDetailSerializer
