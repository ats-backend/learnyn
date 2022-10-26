from django.contrib.auth.models import User

from rest_framework import serializers

from classadmins.models import ClassAdmin
from school.api.serializer import ClassroomSerializer
from school.models import Classroom


class ClassAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    classroom = ClassroomSerializer()
    # classroom = serializers

    class Meta:
        model = ClassAdmin
        fields = (
            'first_name',
            'last_name',
            'email',
            'classroom',
            'is_suspended',
            'is_deleted'
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with that email already exist"
            )
        return value

    def validate_classroom(self, value):
        if ClassAdmin.objects.filter(classroom_id=value).exists():
            raise serializers.ValidationError(
                "That class already has a teacher"
            )
        return value


class AssignClassroomSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Classroom.active_objects.all()
    )

    class Meta:
        model = ClassAdmin
        fields = ('classroom',)

    def validate_classroom(self, value):
        if ClassAdmin.objects.filter(classroom_id=value).exists():
            raise serializers.ValidationError(
                "That class already has a teacher"
            )
        return value