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
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'ingredient',
        'recipe',
    )
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
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


class RecipeFavoritedAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


admin.site.register(models.RecipeFavorited, RecipeFavoritedAdmin)
admin.site.register(models.TagsRecipe, TagsRecipeAdmin)
admin.site.register(models.IngredientsRecipe, IngredientsRecipeAdmin)
admin.site.register(models.Recipes, RecipeAdmin)
admin.site.register(models.Ingredients, IngredientsAdmin)
admin.site.register(models.Tags, TagsAdmin)
