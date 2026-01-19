from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Course, Module


class IsCourseAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModuleAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.course.author == request.user


class IsTaskAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.module.course.author == request.user


class IsCourseAuthorForModuleCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        course_id = view.kwargs.get('pk')
        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            return course.author == request.user
        return False


class IsCourseAuthorForTaskCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        module_id = view.kwargs.get('pk')
        if module_id:
            module = get_object_or_404(Module, pk=module_id)
            return module.course.author == request.user
        return False
