from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model=Course
        fields=['title', 'description', 'is_active', 'created_at', 'author']
        read_only=['created_at', 'author']
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['author'] = request.user
        return super().create(validated_data)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields='__all__'
        read_only = ['created_at']