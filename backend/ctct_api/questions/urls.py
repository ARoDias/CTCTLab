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
router.register(r'studentresponses', views.StudentQuestionnaireResponseViewSet)  
router.register(r'questionresponsedetails', views.QuestionResponseDetailViewSet)  

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', views.task_list, name='task-list'),
    path('activities/<int:activity_id>/questionnaires/', views.get_questionnaires_for_activity, name='activity-questionnaires'),
    path('create_student_responses/', views.create_student_responses, name='create_student_responses'),
    path('stats/', views.question_stats_view, name='question-stats'),
     path('opt_dist/', views.option_distribution_view, name='option-distrib'),
]
