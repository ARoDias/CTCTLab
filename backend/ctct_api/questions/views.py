# backend/ctct_api/questions/views.py
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Activity, Week, FileSubmission
from .serializers import ActivitySerializer, WeekSerializer, FileSubmissionSerializer
from rest_framework.decorators import api_view, permission_classes
from users.models import StudentGroup

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    # ActivityViewSet provides CRUD functions for Activity model

class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    # WeekViewSet is responsible for Week model's CRUD operations

class FileSubmissionViewSet(viewsets.ModelViewSet):
    queryset = FileSubmission.objects.all()
    serializer_class = FileSubmissionSerializer
    # FileSubmissionViewSet is for CRUD of FileSubmission model

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    """
    Return a list of activities related to the authenticated user.
    """
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
    # task_list view provides activity list for authenticated user based on their profile
