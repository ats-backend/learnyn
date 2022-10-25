from django.contrib.auth.models import User

from rest_framework import serializers

from classadmins.models import ClassAdmin
from school.models import Classroom


class ClassAdminSerializer(serializers.ModelSerializer):
    # classroom = serializers

    class Meta:
        model = ClassAdmin
        fields = (
            'first_name',
            'last_name',
            'email',
            'classroom'
        )

    def validate_email(self):
        email = self.validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with that email already exist"
            )
        return email

