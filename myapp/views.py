from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth import login as auth_login, authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        data = request.data
        try:
            CustomUser.objects.get(username=data['username'])
            return Response({"status": "error", "message": f"User with this username address already exists."}, status=400)
        except:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "User created successfully!","data":serializer.data}, status=200)
            
            return Response(serializer.errors, status=400)
        
    def put(self, request, pk=None):
        data = request.data
        try:
            user_obj = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response({"status": "error", "message": f"User Does not exist with ID: {pk}"}, status=400)
        
        serializer = RegisterSerializer(user_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Profile updated successfully!"}, status=200)
        return Response(serializer.errors, status=400)

    
class LoginView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            
            try:
                user_obj = CustomUser.objects.get(username=username)
                if not user_obj.is_active:
                    return Response({"status": "error", "message": "Your account has been disabled!"}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({"status": "error", "message": "The username provided is invalid."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                refresh = RefreshToken.for_user(user)
                
                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'email': user.email,
                    'is_admin': user.is_admin 
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response({"status": "error", "message": "The password provided is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "CustomUser not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if not request.user.is_admin:
            raise PermissionDenied("Only admins can EDIT.")
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not request.user.is_admin:
            raise PermissionDenied("Only admins can delete users.")
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user = request.user
        try:
            Post.objects.get(title=data['title'])
            return Response({"status": "error", "message": f"title with this title  already exists."}, status=400)
        except:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({"status": "success", "message": "post created successfully!","data":serializer.data}, status=200)
            
            return Response(serializer.errors, status=400)