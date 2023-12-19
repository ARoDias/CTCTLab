# questions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity', views.ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', views.task_list, name='task-list'),
]
