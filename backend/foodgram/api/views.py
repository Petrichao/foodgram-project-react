from rest_framework import viewsets

from recipes import models as md
from api.serializers import TagsSerializer, IngredientsSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = md.Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = md.Ingredients.objects.all()
    serializer_class = IngredientsSerializer
