# questions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity', views.ActivityViewSet)
router.register(r'weeks', views.WeekViewSet) 
router.register(r'questionnaires', views.QuestionnaireViewSet) 
router.register(r'questions', views.QuestionViewSet) 
router.register(r'answers', views.AnswerViewSet) 
router.register(r'options', views.OptionViewSet)
router.register(r'questionnairequestions', views.QuestionnaireQuestionViewSet)
 

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', views.task_list, name='task-list'),
]
