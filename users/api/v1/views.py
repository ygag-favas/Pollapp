from rest_framework import generics
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
