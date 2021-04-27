from rest_framework import generics
from .serializers import PollSerializer

from polls.models import Question


class PollList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = PollSerializer
