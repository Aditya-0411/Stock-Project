from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()

            print(f"User {user.username} registered successfully!")
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve username and password from the validated data
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user:
                # Login the user
                login(request, user)

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                print(f"User {username} logged")
                # Return the response
                return Response({
                    "status": "success",
                    "data": {
                        "user": UserSerializer(user).data,
                         "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh)
                    }
                }, status=status.HTTP_200_OK)

            # If authentication fails
            return Response({"status": "error", "data": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # If serializer validation fails
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication to access this view


    def get(self, request):
        # Check if the user has permission to access this view (optional, depends on your requirements)
        if not request.user.is_staff:
            return Response({"status": "error", "data": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve all users
        users = User.objects.all()

        # Serialize the user data
        serializer = UserSerializer(users, many=True)

        # Return the serialized user data
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
