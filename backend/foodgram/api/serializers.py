from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes import models as r_models

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

    class Meta:
        model = r_models.Recipes
        exclude = ('pub_date',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user_id = request.user.id
        recipe_id = obj.id
        return r_models.RecipeFavorited.objects.filter(user=user_id,
                                                       recipe=recipe_id).exists()
