# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'register', views.RegisterViewSet, basename='register')
router.register(r'courses', views.CourseViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.CustomLoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('currentUser', views.current_user, name='current-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
]
