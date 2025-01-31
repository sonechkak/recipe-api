from rest_framework import viewsets, mixins, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.CreateModelMixin):
        """Базовый класс для управления атрибутами рецепта."""
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)

        def get_queryset(self):
            """Возвращает объекты для текущего пользователя."""
            return self.queryset.filter(user=self.request.user).order_by('name')

        def perform_create(self, serializer):
            """Создание нового объекта."""
            serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Управление рецептами."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Управление ингредиентами."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Управление рецептами."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Возвращает объекты для текущего пользователя."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание нового объекта."""
        serializer.save(user=self.request.user)
