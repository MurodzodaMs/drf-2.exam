from django.urls import path
from .views import *

urlpatterns = [
    path('course/', CourseListCreateAPIView.as_view()),
    path('course/<int:pk>', CourseDetailAPIView.as_view()),
    

]