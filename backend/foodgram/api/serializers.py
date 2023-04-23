import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from recipes import models as r_models
from users import models as u_models

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = r_models.Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return u_models.Subscribes.objects.filter(user=user,
                                                  author=obj).exists()


class SubscribeSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('email', 'username')

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if u_models.Subscribes.objects.filter(author=author,
                                              user=user
                                              ).exists():
            raise ValidationError(
                detail='Вы уже подписаны на этого пользователя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = r_models.Tags


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('recipe', 'ingredient', 'amount')
        model = r_models.IngredientsRecipe


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = r_models.Ingredients


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = r_models.Recipes
        exclude = ('pub_date',)
        read_only_fields = ('author',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user_id = request.user.id
        recipe_id = obj.id
        return r_models.RecipeFavorited.objects.filter(
            user=user_id,
            recipe=recipe_id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user_id = request.user.id
        recipe_id = obj.id
        return r_models.ShoppingCart.objects.filter(
            user=user_id,
            recipe=recipe_id
        ).exists()

    def get_ingredients(self, obj):
        recipe = obj

        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientsrecipe__amount')
        )


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = r_models.IngredientsRecipe
        fields = ('id', 'amount')


class RecipesPostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=r_models.Tags.objects.all()
    )
    ingredients = IngredientRecipePostSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = r_models.Recipes
        exclude = ('pub_date',)
        read_only_fields = ('author',)

    def validate_ingredients(self, data):
        ingredients = data
        if not ingredients:
            raise ValidationError({
                'ingredients': 'Нужен хотя бы один ингредиент!'
            })
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(r_models.Ingredients, id=item['id'])
            if ingredient in ingredients_list:
                raise ValidationError({
                    'ingredients': 'Ингридиенты не могут повторяться!'
                })
            if int(item['amount']) <= 0:
                raise ValidationError({
                    'amount': 'Количество ингредиента должно быть больше 0!'
                })
            ingredients_list.append(ingredient)
        return data

    def validate_tags(self, data):
        tags = data
        if not tags:
            raise ValidationError({
                'tags': 'Нужно выбрать хотя бы один тег!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Теги должны быть уникальными!'
                })
            tags_list.append(tag)
        return data

    @transaction.atomic
    def create_ingredients_amounts(self, ingredients, recipe):
        r_models.IngredientsRecipe.objects.bulk_create(
            [r_models.IngredientsRecipe(
                ingredient=r_models.Ingredients.objects.get(id=ingredient[
                    'id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = r_models.Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe,
                                        ingredients=ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(recipe=instance,
                                        ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesSerializer(instance,
                                 context=context).data
