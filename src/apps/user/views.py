from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Создание нового пользователя в системе."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Создание нового токена для пользователя."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # Добавление рендерера для отображения в браузере.


class ManagerUserView(generics.RetrieveUpdateAPIView):
    """Управление аутентификацией пользователя."""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Получение и возврат аутентифицированного пользователя."""
        return self.request.user
