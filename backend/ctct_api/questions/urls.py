# questions/urls.py
# Import necessary modules and classes
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'activity', views.ActivityViewSet)
router.register(r'weeks', views.WeekViewSet)
router.register(r'questionnaires', views.QuestionnaireViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'options', views.OptionViewSet)
router.register(r'questionnairequestions', views.QuestionnaireQuestionViewSet)
router.register(r'studentresponses', views.StudentQuestionnaireResponseViewSet)  # New route for StudentQuestionnaireResponse
router.register(r'questionresponsedetails', views.QuestionResponseDetailViewSet)  # New route for QuestionResponseDetail

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', views.task_list, name='task-list'),
]
