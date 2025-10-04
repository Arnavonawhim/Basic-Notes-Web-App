from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Make Username above 3 chracters")
        if len(value) > 20:
            raise serializers.ValidationError("Make Username less than 20 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain numbers,alphabets and underscore")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Make Password above 7 characters")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Add atleast one uppercase characters")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Add atleast one lowercase character")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Add atleast one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Add atleast one special character")
        return value

    def create(self, validated_data):
        new_user = User.objects.create_user(username=validated_data['username'],email=validated_data.get('email', ''),password=validated_data['password'])
        return new_user


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']