from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from blogs.views import RegisterAPIView, LoginAPIView, get_access_token

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/',get_access_token.as_view()),
]