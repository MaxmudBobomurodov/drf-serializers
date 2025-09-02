from rest_framework import serializers

from app.models import Task, UserProfile


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'