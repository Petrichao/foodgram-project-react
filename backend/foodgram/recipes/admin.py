from django.contrib import admin

from recipes import models


class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class TagsRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tag',
        'recipe',
    )
    search_fields = (
        'recipe',
        'tag',
    )
    empty_value_display = '-пусто-'


class IngredientsRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
    )
    search_fields = (
        'ingredient',
        'recipe',
    )
    empty_value_display = '-пусто-'


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'is_favorited',
        'is_in_shopping_cart',
        'text',
        'pub_date',
        'author',
        'image',
        'cooking_time',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.TagsRecipe, TagsRecipeAdmin)
admin.site.register(models.IngredientsRecipe, IngredientsRecipeAdmin)
admin.site.register(models.Recipes, RecipeAdmin)
admin.site.register(models.Ingredients, IngredientsAdmin)
admin.site.register(models.Tags, TagsAdmin)

