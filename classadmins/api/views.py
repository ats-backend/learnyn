from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import IsSchoolAdmin
from .serializers import ClassAdminSerializer
from classadmins.models import ClassAdmin


class ClassAdminListAPIView(ListCreateAPIView):
    queryset = ClassAdmin.active_objects.all()
    serializer_class = ClassAdminSerializer
    permission_classes = [IsSchoolAdmin]


class ClassAdminDetailAPIView(APIView):
    pass


class AddClassAdminAPIView(APIView):
    pass


class SuspendClassAdminAPIView(APIView):
    pass


class UnassignClassAdminAPIView(APIView):
    pass


class AssignClassAdminAPIView(APIView):
    pass
