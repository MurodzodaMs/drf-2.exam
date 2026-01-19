from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import *


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ['created_at']


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'is_active', 'created_at']


class CourseCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'is_active', 'author']


class CourseSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'is_active',
                  'created_at', 'author', 'modules']
        read_only_fields = ['created_at', 'author', 'modules']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'task_text', 'is_active', 'module']
        read_only_fields = ['module']


class ExampleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Example
        fields = ['task', 'input', 'output']


class ExampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'
        read_only_fields = ['task']


class TrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = '__all__'


class TryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = ['answer']
