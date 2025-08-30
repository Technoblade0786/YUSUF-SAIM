from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

def check_jwt(request):
    token = request.headers.get('Authorization')
    return token == 'valid-jwt-token'  # Placeholder for real token check

class UserProfileAPI(APIView):
    def get(self, request, pk=None):
        if not check_jwt(request):
            return Response({'error': '❌ denied'}, status=status.HTTP_401_UNAUTHORIZED)
        if pk:
            try:
                profile = UserProfile.objects.get(pk=pk)
                serializer = UserProfileSerializer(profile)
                return Response(serializer.data)
            except UserProfile.DoesNotExist:
                return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            profiles = UserProfile.objects.all()
            serializer = UserProfileSerializer(profiles, many=True)
            return Response(serializer.data)

    def post(self, request):
        if not check_jwt(request):
            return Response({'error': '❌ denied'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not check_jwt(request):
            return Response({'error': '❌ denied'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not check_jwt(request):
            return Response({'error': '❌ denied'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile = UserProfile.objects.get(pk=pk)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)