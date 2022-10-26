import json

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView

from classadmins.models import ClassAdmin
from results.api.permissions import IsClassAdminOrSchoolAdmin
from results.api.serializers import ResultListSerializer, ResultCreateSerializer, ResultSerializer, \
    CheckResultTokenSerializer
from results.forms import ResultForm, ResultFormset
from results.models import Result, Token
from results.utils import render_to_pdf, send_mail
from students.models import Student


class ResultListAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            result = Result.objects.all().values_list('student', flat=True)
            student = Student.objects.filter(id__in=result)
        elif ClassAdmin.objects.filter(id=request.user.id).exists():
            result = Result.objects.filter(student__classroom__teacher=request.user).values_list('student', flat=True)
            student = Student.objects.filter(id__in=result)
        else:
            return Response({"error": "You can not access this page"})
        serializer = ResultListSerializer(student, many=True)
        return Response(serializer.data)


class ResultDetailAPIView(RetrieveAPIView):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
    # permission_classes = (IsClassAdminOrSchoolAdmin,)

    def get(self, request, pk):
        print(self.get_object())
        student = Student.objects.get(id=pk)
        result = Result.objects.filter(student=student)
        list(result)
        serializer = ResultSerializer(result, many=True)
        student_name = tuple((f"{i.student.first_name} {i.student.last_name}" for i in result))
        term = tuple((item.term.term for item in result))
        session = tuple((item.session.name_of_session for item in result))
        subjects = [{
            'subject': item.subject.name,
            'first_assessment_score': item.first_assessment_score,
            'second_assessment_score': item.second_assessment_score,
            'exam_score': item.exam_score
        } for item in result]
        return Response({
            'student': student_name[0],
            'term': term[0],
            'session': session[0],
            'results': subjects
        })


class ResultCreateAPIView(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultCreateSerializer
    permission_classes = (permissions.IsAuthenticated, IsClassAdminOrSchoolAdmin)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            student = serializer.data['student']
            student_result = Result.objects.filter(student_id=student)
            student_result_data = [{
                'subject': item.subject.name,
                'first_assessment_score': item.first_assessment_score,
                'second_assessment_score': item.second_assessment_score,
                'exam_score': item.exam_score
            } for item in student_result]
            return Response({
                'success': True,
                **serializer.data,
                'result': student_result_data
            })
        return Response({
            'error': serializer.errors
        })


class CheckResultAPIView(GenericAPIView):
    serializer_class = CheckResultTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CheckResultTokenSerializer(data=request.data)
        print(type(request.data))
        if serializer.is_valid():
            student_token = Token.objects.get(token=serializer.data['user_token'])
            token = Token.objects.filter(token=student_token.token)
            if token.exists() and student_token.count < 6:
                student_token.count += 1
                student_token.save()
                obj = Result.objects.filter(student=student_token.student)
                obj_list = list(obj)
                term = tuple((item.term.term for item in obj))
                session = tuple((item.session.name_of_session for item in obj))
                subjects = [{
                    'subject': item.subject.name,
                    'first_assessment_score': item.first_assessment_score,
                    'second_assessment_score': item.second_assessment_score,
                    'exam_score': item.exam_score
                } for item in obj]
                return Response({
                    'student': str(student_token.student),
                    'term': term[0],
                    'session': session[0],
                    'results': subjects
                })
            return Response({'error': "Token not exist or has expired"})
        return Response({'error': serializer.errors})


class SendResultAPIView(APIView):

    def get(self, request, pk):
        student = Student.objects.get(id=pk)
        generate_result = reverse('result-api:result-detail-api-view', args=[pk])
        pdf_url = str(get_current_site(request)) + generate_result
        subject = f'Download Result'
        send_mail(student, subject, attachment_url=pdf_url)
        return Response({"success": True})



