from django.db import models
from accounts.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='courses'
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, 
        related_name='models', on_delete=models.CASCADE
    )
    order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    task_text = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    


class Example(models.Model):
    task = models.ForeignKey(Task, 
        related_name='examples', on_delete=models.CASCADE
    )
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)


class Try(models.Model):
    STATUS_CHOICES = [
        ("not all", 'NOT ALL'),
        ('error', 'ERROR'),
        ('complete', 'COMPLETE'),
    ]

    user = models.ForeignKey(CustomUser, related_name='tries', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_tries', on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.CharField(
        max_length=50,
        default='Not all',
        choices=STATUS_CHOICES
    )
