from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2'
        ]

    def validate_email(self):
        email = self.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with that email already exist"
            )
        return email

    def validate_username(self):
        email = self.validated_data.get('email')
        username = email.split('@')[0]
        return username

    def validate_password(self):
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return password, password2

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password2)
        user.save()
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def get_token(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    return tokens


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email:
            raise serializers.ValidationError(
                "Email is required"
            )

        if not password:
            raise serializers.ValidationError(
                "Password is required"
            )
        username = email.split('@')[0]
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                "Invalid email or password, please try again"
            )
        data = get_token(user)
        return data


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password2 != password:
            raise serializers.ValidationError(
                "Both passwords must match"
            )
        return attrs
