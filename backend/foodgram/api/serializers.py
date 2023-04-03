from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes import models

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )
        model = User


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = models.Tags


class IngredientsSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = models.Ingredients

    def get_measurement_unit(self, obj):
        return obj.measurement_unit.name

    def get_amount(self, obj):
        return 1


# class IngredSer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     measurement_unit = serializers.CharField()
#     amount = serializers.FloatField()


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientsSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = models.Recipes
        fields = '__all__'


class TagsRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagsRecipe
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IngredientsRecipe
        fields = (
            'ingredient',
            'amount',
            'recipe',
        )
