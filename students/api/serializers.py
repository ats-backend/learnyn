from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import Student
from school.models import Classroom


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    parent_firstname = serializers.CharField(required=True)
    parent_lastname = serializers.CharField(required=True)
    parent_email = serializers.EmailField(required=True)

    # classroom = serializers

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'email',
            'classroom',
            'parent_firstname',
            'parent_lastname',
            'parent_email',
            'is_suspended',
            'is_deleted'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with that email already exist"
            )
        return value

