# backend/ctct_api/users/views.py
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import StudentProfile, TeacherProfile, User, Course, Classroom, StudentGroup
from .serializers import (UserSerializer, CourseSerializer, UserAndProfileRegistrationSerializer, 
                          CustomLoginSerializer,StudentProfileSerializer, TeacherProfileSerializer,
                          ClassroomSerializer, StudentGroupSerializer)
from .utilities import send_activation_email_util
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

# ViewSet for the User model, supporting CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSet for the Course model, supporting CRUD operations
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# ViewSet for the Classroom model, supporting CRUD operations
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

# ViewSet for the StudentProfile model, supporting CRUD operations
class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

# ViewSet for the StudentGroup model, supporting CRUD operations
class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer

# ViewSet for the TeacherProfile model, supporting CRUD operations
class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

# API view to retrieve the currently authenticated user's information
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# API view to handle user login and JWT token generation
class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer
    template_name = 'rest_framework/login.html'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                # Verify if user account is active
                if not user.is_active:
                    return Response({"error": "A conta não se encontra ativa!"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Generate JWT token for authentication
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)

                # Determine user type (student, teacher, admin)
                user_type = "student" if hasattr(user, 'is_student') and user.is_student else "teacher" if hasattr(user, 'is_teacher') and user.is_teacher else "admin" if user.is_superuser else "unauthorized"

                # Create response with token and user type
                response_data = {"key": token, "user_type": user_type, "user_id": user.id} 
                response = JsonResponse(response_data, status=status.HTTP_200_OK)
                response["Authorization"] = f"Bearer {token}"
                
                return response
        return Response({"error": "Número de aluno/username ou password errados!"}, status=status.HTTP_400_BAD_REQUEST)
        # Custom login view to authenticate and provide JWT token

# ViewSet to handle user registration including sending activation emails
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Handles user registration."""
    queryset = User.objects.all()
    serializer_class = UserAndProfileRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.is_student = True
            user.is_teacher = False
            user.save()
            send_activation_email_util(user, request)
            return Response({"message": "Registo feito com sucesso!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # RegisterViewSet for user registration, sends activation email

# ActivateAccount view
class ActivateAccount(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
     
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            print(f"Activation error: {e}")
            return Response({"error": "Erro de ativação."}, status=status.HTTP_400_BAD_REQUEST)

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "A tua conta está ativa, podes fazer login!"}, status=status.HTTP_200_OK)
        else:
            print(f"Invalid token or user not found for UID: {uid}, Token: {token}")
            return Response({"error": "Link de ativação inválido!"}, status=status.HTTP_400_BAD_REQUEST)
        

