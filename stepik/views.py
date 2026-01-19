from django.shortcuts import render, get_object_or_404
from .helper import func
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *
from .permissions import *


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCourseAuthorOrReadOnly]


class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.filter(is_active=True)
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]


# class ModuleCreateAPIView(generics.CreateAPIView):
#     queryset = Module.objects.filter(is_active=True)
#     serializer_class = ModuleSerializer
#     permission_classes = [IsAuthenticated]


class CourseModuleListAPIView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsCourseAuthorForModuleCreate]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ModuleCreateSerializer
        return ModuleSerializer

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Module.objects.filter(course_id=course_id, is_active=True)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        serializer.save(course=course)


class ModuleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.filter(is_active=True)
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsModuleAuthorOrReadOnly]


class ModuleTaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsCourseAuthorForTaskCreate]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        module_id = self.kwargs['pk']
        return Task.objects.filter(module_id=module_id, is_active=True)

    def perform_create(self, serializer):
        module = get_object_or_404(Module, pk=self.kwargs['pk'])
        serializer.save(module=module)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskAuthorOrReadOnly]


class ExampleCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCourseAuthorForTaskCreate]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExampleCreateSerializer
        return ExampleSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        if task_id:
            return Example.objects.filter(task_id=task_id)
        return Example.objects.all()

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        serializer.save(task=task)


class TaskDecideAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TryCreateSerializer

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        examples = Example.objects.filter(task=task)
        data = request.data.copy()

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            try_object = serializer.save(user=request.user, task=task)

            result_status = func(try_object, examples)

            try_object.status = result_status
            try_object.save()

            return Response(TrySerializer(try_object).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
