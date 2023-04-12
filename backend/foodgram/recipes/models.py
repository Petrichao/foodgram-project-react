from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

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
        'Ingredients',
        through='IngredientsRecipe',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        blank=False,
        null=False,
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
        ordering = ('-pub_date',)

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


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = ('Ингредиент для рецепта')
        verbose_name_plural = ('Ингредиенты для рецептов')
        ordering = ('recipe',)


class RecipeFavorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favourite')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Корзину покупок'
