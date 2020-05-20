from rest_framework import serializers
from .models import Question, Choice


# generic api view implement task view


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class MailSerializer(serializers.Serializer):
    maill = serializers.EmailField()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text',)


class ChoiceSerializerWithVotes(ChoiceSerializer):
    class Meta:
        model = Choice
        fields = ('__all__')


class QuestionListPageSerializer(serializers.ModelSerializer):
    was_published_recently = serializers.BooleanField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True)


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
