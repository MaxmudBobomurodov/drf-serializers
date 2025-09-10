from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from blogs.serializers import UserRegisterSerializer, UserLoginSerializer
from blogs.utils import get_tokens_for_user


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'User created',
            'username': serializer.data['username'],
        }, status=status.HTTP_201_CREATED
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response(data=tokens, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class get_access_token(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh_token = request.GET.get('refresh_token')

        if refresh_token is None:
            return Response(
                {
                'message':'No refresh token provided',
            },status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken(refresh_token)
        return Response({
            'access_token': str(refresh.access_token),
        },status=status.HTTP_200_OK)





