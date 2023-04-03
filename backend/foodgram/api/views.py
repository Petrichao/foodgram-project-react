from rest_framework import viewsets, mixins

from recipes import models
from api import  serializers


class GetViewsets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagsViewSet(GetViewsets):
    queryset = models.Tags.objects.all()
    serializer_class = serializers.TagsSerializer


class IngredientsViewSet(GetViewsets):
    queryset = models.Ingredients.objects.all()
    serializer_class = serializers.IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipes.objects.all()
    serializer_class = serializers.RecipesSerializer
