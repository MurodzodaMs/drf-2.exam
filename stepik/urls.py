from django.urls import path
from .views import *

urlpatterns = [
    path('course/', CourseListAPIView.as_view()),
    path('course/create/', CourseCreateAPIView.as_view()),
    path('course/<int:pk>/', CourseDetailAPIView.as_view()),
    path('course/<int:pk>/modules/', CourseModuleListAPIView.as_view()),

    path('module/<int:pk>/', ModuleDetailAPIView.as_view()),
    path('module/<int:pk>/tasks/', ModuleTaskListAPIView.as_view()),

    path('task/<int:pk>/', TaskDetailAPIView.as_view()),
    path('task/<int:pk>/example/', ExampleCreateAPIView.as_view()),
    path('task/<int:pk>/decide/', TaskDecideAPIView.as_view()),
]
