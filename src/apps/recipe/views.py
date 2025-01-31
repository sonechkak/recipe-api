from rest_framework import viewsets, mixins, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe import serializers


class TagViewSet(viewsets.ModelViewSet):
    """Управление рецептами."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Возвращает теги для текущего пользователя."""
        queryset = self.queryset
        assigned_only = bool(self.request.query_params.get('assigned_only'))  # преобразование строки в булево значение
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание нового тега."""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    """Управление ингредиентами."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """Возвращает ингредиенты для текущего пользователя."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Создание нового ингредиента."""
        serializer.save(user=self.request.user)
