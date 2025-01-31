from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
