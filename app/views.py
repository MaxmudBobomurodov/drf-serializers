from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import UserProfile
from app.serializers import UserProfileSerializer


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
            },status=status.HTTP_400_BAD_REQUEST)
