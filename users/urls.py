from django.urls import path
from .views import UserProfileAPI

urlpatterns = [
    path('profiles/', UserProfileAPI.as_view()),
    path('profiles/<int:pk>/', UserProfileAPI.as_view()),
]
