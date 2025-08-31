from django.urls import path

from app.views import UserProfileAPIView

app_name = 'app'

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]