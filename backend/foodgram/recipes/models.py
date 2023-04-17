from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name='Название',
    )
    color = ColorField(default='#FF0000')
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
        unique=False,
        blank=False,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = ('Ингредиент')
        verbose_name_plural = ('Ингредиенты')
        ordering = ('name',)
        constraints = [
            UniqueConstraint(fields=['name', 'measurement_unit'],
                             name='unique_ingrediet')
        ]

    def __str__(self):
        return self.name


class Recipes(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
    )
    text = models.TextField(
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
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

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
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = ('Ингредиент для рецепта')
        verbose_name_plural = ('Ингредиенты для рецептов')
        ordering = ('recipe',)
        constraints = [
            UniqueConstraint(fields=['recipe', 'ingredient'],
                             name='unique_ingredients')
        ]


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
