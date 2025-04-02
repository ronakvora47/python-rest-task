from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','password','city','is_admin']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "is_admin"]
        read_only_fields = ["is_admin"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
    
    
class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False, allow_blank=True)  # Allows blank


    class Meta:
        model = Post
        fields = ['user','title','content','created_at']
