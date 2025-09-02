from datetime import datetime, date

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import UserProfile, Task
from app.serializers import UserProfileSerializer, TaskSerializer


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = UserProfile.objects.get(user=request.user)
        if obj:
            serializer = UserProfileSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "No users found"
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        obj = get_object_or_404(UserProfile, user=request.user)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = UserProfileSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        obj = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        obj = UserProfile.objects.filter(user=request.user).exists()
        if not obj:
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = UserProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "User profile already exists",
            }, status=status.HTTP_400_BAD_REQUEST)


class TaskAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_param = request.query_params.get('status', 'todo')
        priority_param = request.query_params.get('priority', 'high')
        due_date_param = request.query_params.get('due_date')
        if status_param != 'todo':
            return Response(
                {
                    "message": "status should be 'todo' ",
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if priority_param != 'high':
            return Response(
                {
                    "message": "status should be 'high' ",
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if due_date_param:
            try:
                due_date = datetime.strptime(due_date_param, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"message": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if due_date < date.today():
                return Response(
                    {"message": "due date should not be in the past"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        obj = Task.objects.filter(status=status_param, priority=priority_param, due_date=due_date_param)
        serializer = TaskSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk=None):

        obj = get_object_or_404(Task, pk=pk, user=request.user)

        serializer = TaskSerializer(obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        obj = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk=None):
        obj = get_object_or_404(Task, pk=pk, user=request.user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)