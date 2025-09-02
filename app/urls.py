from django.urls import path

from app.views import UserProfileAPIView, TaskAPIView

app_name = 'app'

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('tasks/', TaskAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>', TaskAPIView.as_view(), name='task-detail'),
]