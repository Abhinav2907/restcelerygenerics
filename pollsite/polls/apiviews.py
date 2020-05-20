from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Question, Choice
from .serializers import QuestionListPageSerializer, MailSerializer, QuestionDetailPageSerializer, ChoiceSerializer, \
    VoteSerializer, QuestionResultPageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .tasks import sendmail
from rest_framework import generics


class QuestionsView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListPageSerializer


class TaskView(APIView):
    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        if (serializer.is_valid()):
            email = serializer.validated_data["maill"]
            sendmail.delay(email)
            return Response(status=status.HTTP_201_CREATED)
        sendmail.delay()
        return Response(status=status.HTTP_201_CREATED)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionDetailPageSerializer
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return QuestionSerializer
    #     else:
    #         return QuestionDetailPageSerializer
    lookup_url_kwarg = 'question_id'
    queryset = Question.objects.all()

class QuestionResultView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    lookup_url_kwarg = 'question_id'
    serializer_class = QuestionResultPageSerializer


@api_view(['POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
        choice.votes += 1
        choice.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


