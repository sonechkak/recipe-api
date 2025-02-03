from rest_framework import viewsets, mixins, serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
            assigned_only = bool(
                int(self.request.query_params.get('assigned_only', 0))  # Преобразование строки в число
            )
            queryset = self.queryset
            if assigned_only:
                queryset = queryset.filter(recipe__isnull=False)  # Вывод объектов, которые присвоены рецептам

            return queryset.filter(user=self.request.user).order_by('name').distinct()

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

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание нового объекта."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Возвращает правильный сериализатор."""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Создание нового объекта."""
        serializer.save(user=self.request.user)  # Добавление пользователя к рецепту


    @action(methods=['POST'], detail=True, url_path='upload-image')  # Добавление действия к рецепту
    def upload_image(self, request, pk=None):
        """Загрузка изображения к рецепту."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
