from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tags, through='TagsRecipe')
    ingredients = models.ManyToManyField(Ingredients, through='IngredientsRecipe')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )


class TagsRecipe(models.Model):
    pass


class IngredientsRecipe(models.Model):
    pass


class Recipes(models.Model):
    pass