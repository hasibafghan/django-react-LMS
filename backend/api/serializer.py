from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauths.models import User , Profile
import uuid

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod # ask
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.full_name
        # ...
        return token

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True , validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required = True)
    class Meta:
        model = User
        fields = ('full_name','email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            full_name = validated_data['full_name']
        )

        email_username , domain = validated_data['email'].split('@')
        user.username = f"{email_username}_{uuid.uuid4().hex[:8]}"

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
