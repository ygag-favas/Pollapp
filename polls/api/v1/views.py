from rest_framework import generics
from .serializers import PollSerializer, CommentSerializer

from polls.models import Question
from ...models import Comment


class PollList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = PollSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
