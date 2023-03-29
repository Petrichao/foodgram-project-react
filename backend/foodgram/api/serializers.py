from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Ingredients, IngredientsRecipe, Tags, TagsRecipe, Recipes


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'color', 'slug',)
        model = Tags


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'measurement_unit',)
        model = Ingredients


class RecipesSerializer(serializers.ModelSerializer):
    pass


class TagsRecipesSerializer(serializers.ModelSerializer):
    pass


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    pass
