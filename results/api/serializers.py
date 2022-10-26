from rest_framework import serializers

from results.models import Result, Token
from results.utils import send_mail
from school.models import Classroom, Subject, Term, Session
from students.models import Student


class StudentSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = ('student_id', 'first_name', 'last_name')


class ResultListSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Result
        fields = ('student',)


class SubjectResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('subject', 'first_assessment_score', 'second_assessment_score', 'exam_score')


class ResultCreateSerializer(serializers.ModelSerializer):
    result = SubjectResultSerializer(many=True, required=False)
    # student = StudentSerializer()

    class Meta:
        model = Result
        fields = ('student', 'term', 'session', 'result')

    def validate(self, attrs):
        request = self.context.get('request')
        class_subjects = Subject.objects.filter(classroom__teacher=request.user)

        if len(attrs['result']) != class_subjects.count():
            raise serializers.ValidationError("You have to supply result of all subject for each student")

        if Result.objects.filter(student=attrs['student'], session=attrs['session'], term=attrs['term']).exists():
            raise serializers.ValidationError("Result for the student already exist")

        subjects = []
        for form in attrs['result']:
            subject = form['subject']
            if subject in subjects:
                raise serializers.ValidationError("Results must have distinct subject name")
            subjects.append(subject)

            if subject not in class_subjects:
                raise serializers.ValidationError("You can only add result for the subject in the class")
        return attrs

    def create(self, validated_data):
        current_student = validated_data.get('student')
        current_term = validated_data.get('term')
        current_session = validated_data.get('session')

        if validated_data.get('result'):
            results = validated_data.get('result')
            for result in results:
                obj = Result.objects.create(student=current_student, session=current_session, term=current_term,
                                            **result)
            user_token = Token.objects.create(student=obj.student)
            subject = "Result"
            print(type(user_token.token))
            send_mail(obj.student, subject, user_token=user_token.token)
            return obj


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('student', 'term', 'session', 'subject', 'first_assessment_score', 'second_assessment_score',
                  'exam_score')


# def required(value):
#     if value is None:
#         raise serializers.ValidationError('This field is required')


class CheckResultTokenSerializer(serializers.Serializer):
    user_token = serializers.CharField()
