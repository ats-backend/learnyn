from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from results.api.serializers import ResultSerializer
from results.models import Result
from students.models import Student


class ResultListAPIView(APIView):
    def get(self, request):
        result = Result.objects.filter(student__classroom__teacher=request.user).values_list('student', flat=True)
        student = Student.objects.filter(student_id__in=result)
        serializer = ResultSerializer(student, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
