from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from accounts.api.token import get_token
from accounts.models import ResetPasswordToken


class RegisterAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'username'
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with that email already exist"
            )
        return value

    def validate(self, attrs):
        email = attrs['email']
        attrs['username'] = email.split('@')[0]
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password2)
        user.save()
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


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


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with that email not found"
            )
        return value


class ResetPasswordTokenSerializer(serializers.Serializer):
    token = serializers.IntegerField()

