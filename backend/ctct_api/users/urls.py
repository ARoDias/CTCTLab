# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, CourseViewSet, ClassroomViewSet, 
    StudentProfileViewSet, TeacherProfileViewSet, StudentGroupViewSet, 
    CustomLoginView, current_user, ActivateAccount, RegisterViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'teachers', TeacherProfileViewSet)
router.register(r'studentgroups', StudentGroupViewSet)
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('currentUser/', current_user, name='current-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
