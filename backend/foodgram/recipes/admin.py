from django.contrib import admin

from recipes import models as md


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
        'slug',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


admin.site.register(md.Ingredients, IngredientsAdmin)
admin.site.register(md.Tags, TagsAdmin)

