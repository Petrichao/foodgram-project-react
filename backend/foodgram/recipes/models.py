from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(
        max_length=10,
        verbose_name=('Название'),
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = ('Единицу измерения')
        verbose_name_plural = ('Единицы измерения')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        blank=False,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = ('Тэг')
        verbose_name_plural = ('Тэги')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name='Название',
    )
    measurement_unit = models.ForeignKey(
        Unit,
        related_name='ingredients',
        verbose_name=('Единицы измерения'),
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = ('Ингредиент')
        verbose_name_plural = ('Ингредиенты')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
    )
    text = models.CharField(
        max_length=200,
        blank=False,
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsRecipe',
    )
    ingredients = models.ManyToManyField(
        'IngredientsAmount',
        through='IngredientsRecipe',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True,
    )
    cooking_time = models.IntegerField()

    class Meta:
        verbose_name = ('Рецепт')
        verbose_name_plural = ('Рецепты')
        ordering = ('name',)

    def __str__(self):
        return self.name


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ('Тэг для рецепта')
        verbose_name_plural = ('Теги для рецептов')
        ordering = ('recipe',)


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField()

    def __str__(self):
        obj = self.ingredient
        return obj.name

    class Meta:
        verbose_name = ('Кол-во ингредиета для рецепта')
        verbose_name_plural = ('Кол-во ингредиетов для рецептов')
        ordering = ('ingredient',)


class IngredientsRecipe(models.Model):
    ingredient_amount = models.ForeignKey(
        IngredientsAmount,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ('Ингредиент для рецепта')
        verbose_name_plural = ('Ингредиенты для рецептов')
        ordering = ('recipe',)


class RecipeFavorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_fav',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipe_fav'
    )

    class Meta:
        verbose_name = ('Избранный рецепт пользователя')
        verbose_name_plural = ('Избраннык рецепты пользователей')
        ordering = ('user',)