# backend/ctct_api/questions/views.py

# Import necessary modules and classes

from django.db import transaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .models import (Option, QuestionnaireQuestion, Activity, Week, FileSubmission, 
                     Question, Questionnaire, Answer, ActivityAttempt, 
                     StudentQuestionnaireResponse, QuestionResponseDetail)
from .serializers import (ActivitySerializer, ActivityAttemptSerializer, 
                          WeekSerializer, FileSubmissionSerializer, 
                          QuestionSerializer, QuestionnaireSerializer, 
                          AnswerSerializer, OptionSerializer, 
                          QuestionnaireQuestionSerializer, 
                          StudentQuestionnaireResponseSerializer, DetailedQuestionnaireSerializer,
                          QuestionResponseDetailSerializer, QuestionStatsSerializer,
                          OptionDistributionSerializer)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_student_responses(request):
    serializer = StudentQuestionnaireResponseSerializer(data=request.data)
    if serializer.is_valid():
        student_response = serializer.save()

        response_details_data = request.data.get('response_details')
        for detail_data in response_details_data:
            detail_data['student_response'] = student_response.id  # Add this line
            detail_serializer = QuestionResponseDetailSerializer(data=detail_data)
            if detail_serializer.is_valid():
                detail_serializer.save()
            else:
                print(detail_serializer.errors)  # Debug message
                transaction.set_rollback(True)
                return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  # Debug message
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_stats_view(request):
    question_ids = request.query_params.get('question_ids')
    # Divide a string de IDs e remove espaços vazios
    question_ids = [qid.strip() for qid in question_ids.split(',') if qid.strip()]
    print("question_stats_view log:", question_ids)

    if not all(q_id.isdigit() for q_id in question_ids):
        return Response({'error': 'Invalid question IDs'}, status=400)

    response_data = [
        QuestionStatsSerializer.get_question_stats(int(q_id))
        for q_id in question_ids if q_id
    ]
    return Response(response_data)

@api_view(['GET'])
def option_distribution_view(request):
    question_ids = request.query_params.get('question_ids', '').split(',')
    if not question_ids:
        return Response({'error': 'No question IDs provided'}, status=400)

    data = []
    for qid in question_ids:
        if qid.isdigit():
            distribution = OptionDistributionSerializer.get_option_distribution(int(qid))
            data.append({'question_id': int(qid), 'distribution': distribution})
        else:
            return Response({'error': 'Invalid question IDs'}, status=400)
    return Response(data)


# ViewSet for QuestionResponseDetail model providing CRUD operations
class QuestionResponseDetailViewSet(viewsets.ModelViewSet):
    queryset = QuestionResponseDetail.objects.all()
    serializer_class = QuestionResponseDetailSerializer

class DetailedQuestionnaireViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = DetailedQuestionnaireSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_questionnaires_for_activity(request, activity_id):
    week_number = request.query_params.get('week_number')

    try:
        # Localização da atividade especificada juntamente com a semana
        activity = Activity.objects.get(id=activity_id, week__number=week_number)

        # Filtragem de questionários associados à atividade
        questionnaires = Questionnaire.objects.filter(activity=activity)

        # Serialização dos dados dos questionários
        serializer = DetailedQuestionnaireSerializer(questionnaires, many=True)

        return Response(serializer.data)
    except Activity.DoesNotExist:
        # Logging e resposta em caso de atividade não encontrada
        print(f"A atividade com ID {activity_id} e semana {week_number} não foi encontrada.")
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)