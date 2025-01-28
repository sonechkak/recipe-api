from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Создание нового пользователя в системе."""
    serializer_class = UserSerializer
