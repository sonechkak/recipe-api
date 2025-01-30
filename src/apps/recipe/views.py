from django.shortcuts import render
from rest_framework import viewsets, mixins, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.ModelViewSet):
    """Управление рецептами в БД."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def _params_to_ints(self, qs):
        """Преобразует список строковых идентификаторов в список целых чисел."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Возвращает теги для текущего пользователя."""
        queryset = self.queryset
        assigned_only = bool(self.request.query_params.get('assigned_only'))  # преобразование строки в булево значение
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user)
