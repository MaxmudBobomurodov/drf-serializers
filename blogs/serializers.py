from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password1','password2']

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = password
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')


        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Incorrect username or password')
        attrs['user'] = user
        return attrs