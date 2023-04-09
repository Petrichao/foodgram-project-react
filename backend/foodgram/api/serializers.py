import base64

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes import models as r_models

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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


class IngredientsPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.FloatField()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = r_models.Tags


class IngredientAmountSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.FloatField()

    def get_id(self, obj):
        ing = obj.ingredient
        return ing.id

    def get_name(self, obj):
        ing = obj.ingredient
        return ing.name

    def get_measurement_unit(self, obj):
        ing = obj.ingredient
        mes = ing.measurement_unit
        return mes.name


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = r_models.Ingredients

    def get_measurement_unit(self, obj):
        return obj.measurement_unit.name


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientAmountSerializer(many=True)
    author = AuthorSerializer()
    is_favorited = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = r_models.Recipes
        exclude = ('pub_date',)
        read_only_fields = ('author',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user_id = request.user.id
        recipe_id = obj.id
        return r_models.RecipeFavorited.objects.filter(user=user_id,
                                                       recipe=recipe_id).exists()


class RecipesPostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=r_models.Tags.objects.all()
    )
    ingredients = IngredientsPostSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = r_models.Recipes
        exclude = ('pub_date',)
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = r_models.Recipes.objects.create(**validated_data)

        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            current_ingredient = get_object_or_404(
                r_models.Ingredients,
                pk=ingredient_id
            )
            ingam = r_models.IngredientsAmount.objects.create(
                ingredient=current_ingredient,
                amount=ingredient.get('amount')
            )
            ingam.save()
            r_models.IngredientsRecipe.objects.create(
                ingredient_amount=ingam,
                recipe=recipe
            )

        for tag in tags:
            r_models.TagsRecipe.objects.create(
                tag=tag,
                recipe=recipe
            )
        return recipe

