from rest_framework import serializers

from results.models import Result, Token


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('student', 'term', 'session', 'subject', 'first_assessment_score', 'second_assessment_score',
                  'exam_score')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('student', 'token', 'count')
