from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
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

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=10,
        unique=True,
        blank=False,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return self.name


class Recipes(models.Model):
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
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
        Ingredients,
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


class TagsRecipe(models.Model):
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    volume = models.FloatField()
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
    )
